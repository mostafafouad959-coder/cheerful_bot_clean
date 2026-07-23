import os
import pickle
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise        import cosine_similarity

from core.nlp_cleaner import clean_text, clean_text_for_model
from core.translator  import prepare_for_classifier, check_dependencies
from core.database    import get_all_cases, add_case
from core.responses   import get_response

BASE         = os.path.dirname(__file__)
MODEL_DIR    = os.path.join(BASE, "..", "model")
CLASSIFIER_P = os.path.join(MODEL_DIR, "emotion_classifier.pkl")
TFIDF_P      = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
INDEX_P      = os.path.join(MODEL_DIR, "case_index.pkl")

_classifier  = None
_vectorizer  = None
_matrix      = None
_case_ids:   list[int] = []
_categories: list[str] = []


# Small backup detector. The ML model is still the main detector, but this
# prevents the app from showing "neutral" for clear emotional sentences when
# the pickle cannot load or the model is not confident.
EMOTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "sadness": (
        "sad", "unhappy", "depressed", "depression", "cry", "crying", "hurt",
        "pain", "lonely", "alone", "lost", "broken", "hopeless", "miserable",
        "not happy", "no joy",
    ),
    "anger": (
        "angry", "anger", "mad", "furious", "rage", "annoyed", "frustrated",
        "irritated",
    ),
    "hate": ("hate", "hated", "disgust", "resent"),
    "empty": ("empty", "numb", "nothing", "blank", "feel nothing", "no feelings"),
    "anxiety": (
        "anxious", "anxiety", "worried", "worry", "scared", "afraid", "fear",
        "panic", "stressed", "stress", "nervous", "overthinking",
    ),
    "happiness": (
        "happy", "happiness", "joy", "joyful", "glad", "great", "good",
        "amazing", "wonderful", "excited",
    ),
    "love": ("love", "loved", "loving", "care", "caring"),
    "relief": ("relieved", "relief", "calm", "better now"),
    "enthusiasm": ("enthusiastic", "motivated", "ready", "energetic"),
    "fun": ("fun", "funny", "laugh", "laughing", "enjoy"),
    "surprise": ("surprised", "shock", "shocked", "wow"),
}


def _keyword_emotion(text: str, cleaned: str = "") -> tuple[str | None, float]:
    haystack = f"{text.lower()} {cleaned.lower()}"
    haystack = re.sub(r"\s+", " ", haystack)

    best_emotion = None
    best_hits = 0

    for emotion, keywords in EMOTION_KEYWORDS.items():
        hits = 0
        for keyword in keywords:
            if " " in keyword:
                hits += int(keyword in haystack)
            else:
                hits += int(re.search(rf"\b{re.escape(keyword)}\w*\b", haystack) is not None)

        if hits > best_hits:
            best_emotion = emotion
            best_hits = hits

    if best_emotion is None:
        return None, 0.0

    return best_emotion, min(0.98, 0.72 + (best_hits * 0.08))


def _load_classifier():
    global _classifier
    if _classifier is None and os.path.exists(CLASSIFIER_P):
        with open(CLASSIFIER_P, "rb") as f:
            _classifier = pickle.load(f)
    return _classifier


def _load_index():
    global _vectorizer, _matrix, _case_ids, _categories
    with open(TFIDF_P, "rb") as f:
        _vectorizer = pickle.load(f)
    with open(INDEX_P, "rb") as f:
        _matrix, _case_ids, _categories = pickle.load(f)


def _ensure_index_loaded():
    if _vectorizer is None:
        build_index()


def build_index(force: bool = False) -> None:
    global _vectorizer, _matrix, _case_ids, _categories

    if not force and os.path.exists(TFIDF_P) and os.path.exists(INDEX_P):
        _load_index()
        return

    print("[cbr_engine] Building TF-IDF index…")
    cases = get_all_cases()
    if not cases:
        raise RuntimeError("Database is empty — run database.init_db() first.")

    cleaned     = [clean_text(c["User_Input"]) for c in cases]
    _case_ids   = [c["id"]       for c in cases]
    _categories = [c["Category"] for c in cases]

    _vectorizer = TfidfVectorizer(max_features=15_000, ngram_range=(1, 2), sublinear_tf=True)
    _matrix     = _vectorizer.fit_transform(cleaned)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(TFIDF_P, "wb") as f:
        pickle.dump(_vectorizer, f)
    with open(INDEX_P, "wb") as f:
        pickle.dump((_matrix, _case_ids, _categories), f)

    print(f"[cbr_engine] Index built: {len(cases):,} cases, {_matrix.shape[1]:,} features.")


def classify_emotion(text: str, debug: bool = False) -> dict:
    clf = _load_classifier()

    if debug:
        print()
        print("─" * 60)
        print(f"  [cbr] Input: {text!r}")

    english_text, detected_lang, translated, translation_ok = prepare_for_classifier(
        text, debug=debug
    )

    cleaned = clean_text_for_model(english_text, debug=debug)

    keyword_emotion, keyword_confidence = _keyword_emotion(
        f"{text} {english_text}", cleaned
    )

    source = "model"
    if clf is None:
        print("  [cbr] WARNING: emotion_classifier.pkl not found.")
        emotion = keyword_emotion or "neutral"
        confidence = keyword_confidence or 0.5
        source = "keywords" if keyword_emotion else "fallback"
    else:
        emotion    = clf.predict([cleaned])[0]
        proba      = clf.predict_proba([cleaned])[0]
        confidence = float(proba.max())

        if keyword_emotion and (
            emotion == "neutral"
            or confidence < 0.55
            or (keyword_confidence >= 0.88 and emotion != keyword_emotion)
        ):
            emotion = keyword_emotion
            confidence = max(confidence, keyword_confidence)
            source = "keywords"
        elif not keyword_emotion and confidence < 0.55:
            emotion = "neutral"
            source = "low-confidence"

    if debug:
        print(f"  [cbr] Predicted emotion : {emotion}  ({confidence*100:.1f}% confidence, {source})")

    return {
        "emotion":         emotion,
        "confidence":      confidence,
        "detected_lang":   detected_lang,
        "translated_text": translated,
        "translation_ok":  translation_ok,
        "cleaned_text":    cleaned,
        "source":          source,
    }


def retrieve_similar(user_input: str) -> float:
    _ensure_index_loaded()
    english_text, _, _, _ = prepare_for_classifier(user_input)
    cleaned = clean_text(english_text)
    vec     = _vectorizer.transform([cleaned])
    scores  = cosine_similarity(vec, _matrix).flatten()
    return float(scores.max())


def query(user_input: str, ui_lang: str = "en", debug: bool = False) -> dict:
    clf_result = classify_emotion(user_input, debug=debug)

    emotion         = clf_result["emotion"]
    confidence      = clf_result["confidence"]
    detected_lang   = clf_result["detected_lang"]
    translated_text = clf_result["translated_text"]
    translation_ok  = clf_result["translation_ok"]
    cleaned_text    = clf_result["cleaned_text"]
    source          = clf_result["source"]

    sim_score = retrieve_similar(user_input)
    response  = get_response(emotion, lang=ui_lang)

    return {
        "response":        response,
        "category":        emotion,
        "confidence":      confidence,
        "score":           sim_score,
        "id":              -1,
        "detected_lang":   detected_lang,
        "translated_text": translated_text,
        "translation_ok":  translation_ok,
        "cleaned_text":    cleaned_text,
        "source":          source,
    }


def retain(user_input: str, approved_response: str, category: str) -> int:
    new_id = add_case(user_input, approved_response, category)
    build_index(force=True)
    return new_id


if __name__ == "__main__":
    from core.database import init_db

    print("Dependency check:", check_dependencies())
    print()

    csv_path = os.path.join(BASE, "..", "data", "10_emotions_dataset.csv")
    init_db(csv_path)
    build_index()

    test_cases = [
        ("I am not happy at all",                 "en", "sadness"),
        ("I feel lost and alone",                 "en", "sadness"),
        ("I can't feel any joy",                  "en", "sadness"),
        ("Nothing makes me feel better",          "en", "sadness"),
        ("I am so happy today",                   "en", "happiness"),
        ("I love spending time with family",      "en", "love"),
        ("أنا حزين جداً",                         "ar", "sadness"),
        ("أنا سعيد اليوم",                        "ar", "happiness"),
        ("لا أستطيع أن أشعر بالسعادة",           "ar", "sadness"),
        ("Je suis très triste",                   "fr", "sadness"),
        ("Je me sens seul et perdu",              "fr", "sadness"),
        ("Je suis tellement heureux aujourd'hui", "fr", "happiness"),
    ]

    correct = 0
    for text, ui_lang, expected in test_cases:
        r = query(text, ui_lang=ui_lang, debug=True)
        match = "✅" if r["category"] == expected else "❌"
        print(f"  {match} Predicted: {r['category']:12s}  Expected: {expected:12s}  "
              f"Confidence: {r['confidence']*100:.1f}%")
        if r["category"] == expected:
            correct += 1

    print(f"\n  Score: {correct}/{len(test_cases)}")
