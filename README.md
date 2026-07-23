# Cheerful Bot

Cheerful Bot is a simple Streamlit mental-health support chatbot.
It detects the user's emotion, chooses a supportive response, and can learn
from helpful answers with the thumbs-up button.

## Run

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Main Files

- `app/streamlit_app.py` - the new mint-green Streamlit UI.
- `core/cbr_engine.py` - emotion detection, model loading, keyword backup, and response flow.
- `core/responses.py` - supportive responses for each emotion.
- `core/database.py` - SQLite case storage.
- `data/` - dataset and database.
- `model/` - saved classifier and TF-IDF index files.
- `voice/` - optional voice input.

## Notes

The ML classifier is the main detector. If it cannot load or is unsure, the
keyword backup prevents obvious emotional messages from being marked as neutral.
