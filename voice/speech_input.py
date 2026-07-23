import numpy as np

try:
    import sounddevice as sd
    SD_AVAILABLE = True
    SD_ERROR = ""
except (ImportError, OSError) as e:
    SD_AVAILABLE = False
    SD_ERROR = str(e)

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

VOICE_READY = SD_AVAILABLE and SR_AVAILABLE

INSTALL_GUIDE = """
sounddevice or SpeechRecognition is not installed.

Run this ONE command in your terminal:

    pip install sounddevice SpeechRecognition numpy

Then restart Streamlit — voice input will work automatically.
No C++ compiler or Build Tools required.
"""

SUPPORTED_LANGUAGES = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Arabic":       "ar-SA",
    "French":       "fr-FR",
    "Spanish":      "es-ES",
    "German":       "de-DE",
    "Italian":      "it-IT",
    "Japanese":     "ja-JP",
    "Chinese":      "zh-CN",
    "Portuguese":   "pt-BR",
}

_SAMPLE_RATE = 16_000


class VoiceInput:
    def __init__(self, language: str = "en-US", duration: int = 6):
        if not VOICE_READY:
            missing = []
            if not SD_AVAILABLE:
                missing.append("sounddevice")
            if not SR_AVAILABLE:
                missing.append("SpeechRecognition")
            raise RuntimeError(
                f"Missing packages: {', '.join(missing)}\n{INSTALL_GUIDE}"
            )
        self.language   = language
        self.duration   = duration
        self.recogniser = sr.Recognizer()

    def listen(self) -> str:
        try:
            print(f"[MindCare AI] Recording for {self.duration}s — speak now!")
            recording = sd.rec(
                int(self.duration * _SAMPLE_RATE),
                samplerate=_SAMPLE_RATE,
                channels=1,
                dtype="int16",
            )
            sd.wait()
            print("[MindCare AI] Recording done. Transcribing…")

        except sd.PortAudioError as e:
            return f"ERROR: Microphone not accessible — {e}"
        except Exception as e:
            return f"ERROR: Recording failed — {e}"

        raw_bytes  = recording.tobytes()
        audio_data = sr.AudioData(raw_bytes, _SAMPLE_RATE, sample_width=2)

        try:
            text = self.recogniser.recognize_google(
                audio_data, language=self.language
            )
            print(f"[MindCare AI] Heard: {text}")
            return text
        except sr.UnknownValueError:
            return "ERROR: Could not understand audio. Please speak clearly and try again."
        except sr.RequestError as e:
            return f"ERROR: Google Speech API unavailable — {e}"

    def set_language(self, code: str) -> None:
        self.language = code


def check_voice() -> tuple[bool, str]:
    if not SR_AVAILABLE:
        return False, "SpeechRecognition not installed.\nRun: pip install SpeechRecognition"
    if not SD_AVAILABLE:
        return False, (
            "sounddevice not installed or PortAudio missing.\n"
            "Run: pip install sounddevice numpy\n\n"
            f"Original error: {SD_ERROR}"
        )
    return True, "Voice input ready ✓"


def get_language_code(display_name: str) -> str:
    return SUPPORTED_LANGUAGES.get(display_name, "en-US")


if __name__ == "__main__":
    ok, msg = check_voice()
    if not ok:
        print("Voice unavailable:", msg)
    else:
        vi     = VoiceInput(language="en-US", duration=5)
        result = vi.listen()
        print("Result:", result)
