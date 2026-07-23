import re

try:
    from langdetect import detect as _ld_detect, LangDetectException
    _LANGDETECT_OK = True
except ImportError:
    _LANGDETECT_OK = False

try:
    from deep_translator import GoogleTranslator
    _TRANSLATOR_OK = True
except ImportError:
    _TRANSLATOR_OK = False

SUPPORTED_LANG_CODES: dict[str, str] = {
    "en": "English",
    "ar": "Arabic / العربية",
    "fr": "French / Français",
}

_AR_RE = re.compile(r"[\u0600-\u06FF]")

_FR_RE = re.compile(
    r"\b(je|tu|il|elle|nous|vous|ils|elles|est|sont|très|suis|pas|pour|avec"
    r"|dans|sur|je suis|c'est|je me|mon|ma|mes|un|une|les|des|du|au|aux|en"
    r"|ou|et|mais|donc|car|parce|aussi|plus|comme|quand|bien|tout|même|autre"
    r"|être|avoir|faire|voir|vouloir|pouvoir|aller|venir|prendre|savoir)\b",
    re.IGNORECASE,
)


def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"

    stripped = text.strip()

    if _AR_RE.search(stripped):
        return "ar"

    if _FR_RE.search(stripped):
        return "fr"

    if _LANGDETECT_OK:
        try:
            code = _ld_detect(stripped)
            return code if code in SUPPORTED_LANG_CODES else "en"
        except LangDetectException:
            pass

    return "en"


def translate_to_english(text: str, source_lang: str) -> tuple[str, bool]:
    if source_lang == "en":
        return text, True

    if not _TRANSLATOR_OK:
        print(
            "[translator] WARNING: deep-translator not installed.\n"
            "  Run: pip install deep-translator\n"
            "  Falling back to original text — emotion accuracy will be lower."
        )
        return text, False

    try:
        translator = GoogleTranslator(source=source_lang, target="en")
        result     = translator.translate(text)

        if not result or not result.strip():
            raise ValueError("GoogleTranslator returned an empty string.")

        return result.strip(), True

    except Exception as exc:
        print(f"[translator] Translation failed ({source_lang} → en): {exc}")
        print(f"[translator] Fallback: using original text → '{text}'")
        return text, False


def prepare_for_classifier(
    text: str,
    debug: bool = False,
) -> tuple[str, str, str, bool]:
    lang = detect_language(text)

    if debug:
        lang_name = SUPPORTED_LANG_CODES.get(lang, lang)
        print(f"  [translator] Detected  : {lang} ({lang_name})")
        print(f"  [translator] Original  : {text}")

    english_text, ok = translate_to_english(text, source_lang=lang)

    if debug:
        if lang != "en":
            status = "✅ OK" if ok else "❌ FAILED (using original)"
            print(f"  [translator] Translated: {english_text}  [{status}]")
        else:
            print(f"  [translator] No translation needed (input is English).")

    return english_text, lang, english_text, ok


def check_dependencies() -> dict[str, bool]:
    return {
        "langdetect":      _LANGDETECT_OK,
        "deep-translator": _TRANSLATOR_OK,
    }


if __name__ == "__main__":
    deps = check_dependencies()
    print("Dependency check:", deps)
    print()

    cases = [
        "I am not happy at all",
        "I feel lost and alone",
        "أنا حزين جداً",
        "لا أستطيع أن أشعر بالسعادة",
        "أنا سعيد جداً اليوم",
        "Je suis très triste",
        "Je me sens tellement seul et perdu",
        "Je ne me sens pas bien",
        "Je suis tellement heureux aujourd'hui",
    ]

    print("=" * 65)
    for inp in cases:
        print(f"\nInput: {inp}")
        en, lang, translated, ok = prepare_for_classifier(inp, debug=True)
        print(f"  → English for model: '{en}'  (lang={lang}, ok={ok})")
