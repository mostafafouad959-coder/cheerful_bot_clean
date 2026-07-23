import re


_NEGATION_TRIGGERS = {
    "not", "no", "nor", "never", "nobody", "nothing", "nowhere", "neither",
    "cannot",
}

EMOTION_CRITICAL_WORDS = {
    "not", "no", "nor", "never", "nobody", "nothing", "nowhere", "neither",
    "very", "so", "really", "extremely", "absolutely", "totally", "completely",
    "deeply", "truly", "terribly", "awfully", "incredibly", "quite", "too",
    "almost", "barely", "hardly", "scarcely",
    "wrong", "bad", "worse", "worst", "lost", "alone", "empty",
}

_RAW_STOPWORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those","am","is","are",
    "was","were","be","been","being","have","has","had","having","do","does",
    "did","doing","a","an","the","and","but","if","or","because","as","until",
    "while","of","at","by","for","with","about","against","between","into",
    "through","during","before","after","above","below","to","from","up","down",
    "in","out","on","off","over","under","again","further","then","once","here",
    "there","when","where","why","how","all","both","each","few","more","most",
    "other","some","such","s","t","can","will","just","should","now","d","ll",
    "m","o","re","ve","y","ain","aren","couldn","didn","doesn","hadn","hasn",
    "haven","isn","ma","mightn","mustn","needn","shan","shouldn","wasn","weren",
    "won","wouldn","feel","feeling","felt","like","get","got","make","made",
    "would","could","thing","things","way","time","know","think",
}

SAFE_STOPWORDS = _RAW_STOPWORDS - EMOTION_CRITICAL_WORDS

_CONTRACTIONS = {
    r"\bcan't\b":    "can not",
    r"\bcannot\b":   "can not",
    r"\bwon't\b":    "will not",
    r"\bdon't\b":    "do not",
    r"\bdoesn't\b":  "does not",
    r"\bdidn't\b":   "did not",
    r"\bisn't\b":    "is not",
    r"\baren't\b":   "are not",
    r"\bwasn't\b":   "was not",
    r"\bweren't\b":  "were not",
    r"\bhaven't\b":  "have not",
    r"\bhadn't\b":   "had not",
    r"\bwouldn't\b": "would not",
    r"\bcouldn't\b": "could not",
    r"\bshouldn't\b":"should not",
    r"\bmustn't\b":  "must not",
    r"\bneedn't\b":  "need not",
    r"\bI'm\b":      "I am",
    r"\byou're\b":   "you are",
    r"\bhe's\b":     "he is",
    r"\bshe's\b":    "she is",
    r"\bit's\b":     "it is",
    r"\bwe're\b":    "we are",
    r"\bthey're\b":  "they are",
    r"\bI've\b":     "I have",
    r"\bI'll\b":     "I will",
    r"\bI'd\b":      "I would",
}

def _expand_contractions(text: str) -> str:
    for pattern, replacement in _CONTRACTIONS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


_MAX_SKIP = 3

_SKIP_ON_NEG = {
    "a","an","the",
    "i","you","he","she","it","we","they",
    "am","is","are","was","were","be","been","being",
    "do","does","did","have","has","had","will","would","could","should",
    "my","your","his","her","its","our","their",
    "ever","just","even","still",
}

def _apply_negation_tagging(tokens: list[str]) -> list[str]:
    result: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok in _NEGATION_TRIGGERS:
            fused   = False
            skip    = 1
            while skip <= _MAX_SKIP and (i + skip) < len(tokens):
                candidate = tokens[i + skip]
                if candidate not in _SKIP_ON_NEG and candidate not in _NEGATION_TRIGGERS:
                    result.append(f"NOT_{candidate}")
                    i += skip + 1
                    fused = True
                    break
                skip += 1

            if not fused:
                result.append(tok)
                i += 1
        else:
            result.append(tok)
            i += 1

    return result


_LEMMA_RULES = [
    (r"ies$",    "y"),
    (r"ied$",    "y"),
    (r"ing$",    ""),
    (r"ness$",   ""),
    (r"ment$",   ""),
    (r"tion$",   ""),
    (r"ations$", ""),
    (r"ated$",   "ate"),
    (r"ed$",     ""),
    (r"er$",     ""),
    (r"est$",    ""),
    (r"ly$",     ""),
    (r"s$",      ""),
]

def _lemmatize(word: str) -> str:
    if word.startswith("NOT_"):
        return word
    if len(word) <= 3:
        return word
    for pattern, replacement in _LEMMA_RULES:
        new = re.sub(pattern, replacement, word)
        if new != word and len(new) > 2:
            return new
    return word


def clean_text(text: str, debug: bool = False) -> str:
    if debug:
        print(f"  [cleaner] Original text          : {text}")

    text = _expand_contractions(text)
    text = text.lower()
    text = re.sub(r"[^a-z_\s]", " ", text)
    tokens = text.split()
    tokens = _apply_negation_tagging(tokens)

    if debug:
        print(f"  [cleaner] After negation tagging : {' '.join(tokens)}")

    tokens = [
        t for t in tokens
        if t.startswith("NOT_") or (t not in SAFE_STOPWORDS and len(t) > 1)
    ]
    tokens = [_lemmatize(t) for t in tokens]
    tokens = [t for t in tokens if len(t) > 1]

    result = " ".join(tokens)

    if debug:
        print(f"  [cleaner] Final cleaned text     : {result}")

    return result


def clean_text_for_model(text: str, debug: bool = False) -> str:
    return clean_text(text, debug=debug)


if __name__ == "__main__":
    test_cases = [
        ("I am not happy at all",                "[expect: NOT_happy — sadness]"),
        ("I can't feel any joy",                 "[expect: NOT_feel — sadness]"),
        ("I don't want to go outside",           "[expect: NOT_want — sadness/empty]"),
        ("Nothing makes me feel better",         "[expect: NOT_make — sadness]"),
        ("I never feel good enough",             "[expect: NOT_feel — sadness]"),
        ("I won't be happy again",               "[expect: NOT_happy — sadness]"),
        ("I'm not okay at all",                  "[expect: NOT_okay — sadness]"),
        ("I am so happy today",                  "[expect: happy — happiness]"),
        ("I feel really excited",                "[expect: NOT_excited — enthusiasm]"),
        ("I love spending time with my family",  "[expect: love — love]"),
        ("I feel lost and alone",                "[expect: lost alone — sadness]"),
        ("I feel so empty inside",               "[expect: empty — empty]"),
        ("I am very sad",                        "[translated from Arabic/French]"),
        ("I can not feel happiness",             "[translated negation]"),
    ]

    print("=" * 70)
    print("  nlp_cleaner self-test  —  negation tagging pipeline")
    print("=" * 70)
    for text, note in test_cases:
        print(f"\n  {note}")
        clean_text(text, debug=True)
