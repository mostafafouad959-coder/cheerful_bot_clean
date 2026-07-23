import re
import random
from core.database import CHEERFUL_PREFIXES

NEGATIVE_WORDS_EN = {
    "sad","sadness","depress","depressed","depression","cry","crying","hurt",
    "pain","suffer","miserable","awful","terrible","horrible","hate","angry",
    "anger","rage","furious","empty","lonely","alone","lost","broken","hopeless",
    "worthless","useless","ugly","stupid","failure","failed","bad","worst",
    "anxious","anxiety","scared","afraid","fear","worried","worry","stressed",
    "stress","exhausted","tired","shame","embarrassed","guilty","grief","grieve",
}
POSITIVE_WORDS_EN = {
    "happy","happiness","joy","joyful","love","excited","great","wonderful",
    "amazing","fantastic","awesome","fun","laugh","smile","grateful","thankful",
    "proud","hope","hopeful","good","best","excellent","brilliant","cheerful",
    "relief","relieved","pleased","glad","thrilled","enthusiastic",
}

NEGATIVE_WORDS_AR = {
    "حزين","حزينة","حزن","وحيد","وحيدة","ضايع","ضايعة","مكسور","مكسورة",
    "يأس","يائس","خايف","خايفة","قلق","قلقان","غاضب","غاضبة","غضب","كره",
    "بكري","بابكي","تعبان","تعبانة","ألم","بيوجعني","فاضي","فراغ",
    "مش تمام","بحس بألم","مفيش أمل","تعب","خوف","وجع",
}
POSITIVE_WORDS_AR = {
    "سعيد","سعيدة","سعادة","فرحان","فرحانة","فرح","بحب","محبة","حب",
    "ممتاز","رائع","رائعة","كويس","كويسة","متحمس","متحمسة","أمل",
    "شكر","ممنون","ممنونة","بهجة","ارتياح","مرتاح","مرتاحة",
}

NEGATIVE_WORDS_FR = {
    "triste","tristesse","seul","seule","perdu","perdue","cassé","cassée",
    "désespoir","désespéré","peur","anxieux","anxieuse","colère","haine",
    "souffrir","douleur","horrible","terrible","nul","nulle","mauvais",
    "pleure","pleurer","fatigué","fatiguée","honte","coupable","vide",
    "inquiet","inquiète","stressé","stressée","malheureux","malheureuse",
}
POSITIVE_WORDS_FR = {
    "heureux","heureuse","bonheur","joie","joyeux","joyeuse","amour",
    "excellent","magnifique","super","formidable","bien","merci",
    "content","contente","enthousiaste","espoir","soulagé","soulagée",
    "fier","fière","reconnaissant","reconnaissante","ravi","ravie",
}

EMOTION_TO_SENTIMENT = {
    "sadness":"negative",
    "anger":"negative",
    "hate":"negative",
    "empty":"negative",
    "anxiety":"negative",
    "fun":"positive",
    "happiness":"positive",
    "love":"positive",
    "enthusiasm":"positive",
    "relief":"positive",
    "surprise":"neutral",
    "neutral":"neutral",
}

_AR_RANGE = re.compile(r'[\u0600-\u06FF]')
_FR_HINTS  = re.compile(r'\b(je|tu|il|elle|nous|vous|ils|elles|est|sont|très|bien|pas|pour|avec|dans|sur|je suis|c\'est)\b', re.I)

def detect_language(text: str) -> str:
    if _AR_RANGE.search(text):
        return "ar"
    if _FR_HINTS.search(text):
        return "fr"
    return "en"


def analyse_sentiment(text: str, lang: str | None = None) -> str:
    if lang is None:
        lang = detect_language(text)

    words_raw = re.findall(r'\w+', text.lower())

    if lang == "ar":
        neg_set = NEGATIVE_WORDS_AR
        pos_set = POSITIVE_WORDS_AR
    elif lang == "fr":
        neg_set = NEGATIVE_WORDS_FR
        pos_set = POSITIVE_WORDS_FR
    else:
        neg_set = NEGATIVE_WORDS_EN
        pos_set = POSITIVE_WORDS_EN

    if lang == "ar":
        pos = sum(1 for w in words_raw if any(p in w for p in pos_set))
        neg = sum(1 for w in words_raw if any(n in w for n in neg_set))
    else:
        pos = sum(1 for w in words_raw if w in pos_set)
        neg = sum(1 for w in words_raw if w in neg_set)

    if neg > pos:
        return "negative"
    elif pos > neg:
        return "positive"
    return "neutral"


def sentiment_from_emotion(emotion: str) -> str:
    return EMOTION_TO_SENTIMENT.get(emotion.lower(), "neutral")


def add_cheerful_prefix(response: str, emotion: str) -> str:
    prefixes = CHEERFUL_PREFIXES.get(emotion.lower(), ["Here for you! 💙 "])
    prefix   = random.choice(prefixes)

    for p in CHEERFUL_PREFIXES.values():
        for item in p:
            if response.startswith(item[:10]):
                return response

    return prefix + response


def build_cheerful_response(raw_response: str, emotion: str,
                             lang: str | None = None) -> str:
    sentiment = sentiment_from_emotion(emotion)
    if sentiment == "negative":
        return add_cheerful_prefix(raw_response, emotion)
    return raw_response


if __name__ == "__main__":
    tests = [
        ("I feel so lonely and broken today",           None),
        ("أنا حاسس بحزن شديد ومش لاقي حد يتكلم معايا", None),
        ("Je me sens tellement seul et perdu",          None),
        ("I am thrilled about the results!",            None),
        ("Not sure how I feel about it",                None),
    ]
    for text, lang in tests:
        detected_lang = detect_language(text) if lang is None else lang
        sentiment     = analyse_sentiment(text, lang=detected_lang)
        print(f"Text     : {text}")
        print(f"Lang     : {detected_lang}  |  Sentiment: {sentiment}")
        print()
