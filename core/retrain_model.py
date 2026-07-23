import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from core.nlp_cleaner import clean_text_for_model

def prepare_training_data(csv_path):
    df = pd.read_csv(csv_path)
    df['cleaned_text'] = df['text'].apply(lambda x: clean_text_for_model(str(x)))
    df = df[df['cleaned_text'].str.len() > 2]
    return df

def train_model(csv_path, model_path="model/emotion_classifier.pkl"):
    print("Loading and preprocessing data...")
    df = prepare_training_data(csv_path)

    X = df['cleaned_text']
    y = df['emotion']

    print(f"Training on {len(X)} samples")
    print(f"Emotion distribution:\n{y.value_counts()}")

    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 3),
        sublinear_tf=True,
        min_df=3,
        max_df=0.95
    )

    classifier = LogisticRegression(
        C=1.0,
        max_iter=1000,
        multi_class='ovr',
        class_weight='balanced'
    )

    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('clf', classifier)
    ])

    print("Training model...")
    pipeline.fit(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    print("\nModel Performance:")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    pipeline.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"\nModel saved to {model_path}")

    test_examples = [
        "I am not happy",
        "I can't feel happy",
        "I feel lost and alone",
        "This is not good",
        "I don't like this feeling",
    ]

    print("\nTesting negation examples:")
    for example in test_examples:
        cleaned = clean_text_for_model(example)
        pred = pipeline.predict([cleaned])[0]
        prob = pipeline.predict_proba([cleaned])[0].max()
        print(f"  '{example}' → {pred} ({prob:.1%})")

if __name__ == "__main__":
    csv_path = "data/10_emotions_dataset.csv"
    train_model(csv_path)
