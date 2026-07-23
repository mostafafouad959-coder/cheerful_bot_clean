import sqlite3
import csv
import os
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cheerful_bot.db")

CHEERFUL_PREFIXES = {
    "sadness":    ["I'm so proud of you for talking to me! 💙 ",
                   "It takes courage to share this. 🌟 ",
                   "You are stronger than you think! 💪 "],
    "anger":      ["Take a deep breath — you've got this! 🌬️ ",
                   "Your feelings are valid. Let's work through it. ✨ "],
    "hate":       ["Sending you kindness right now. 🤗 ",
                   "You deserve peace and happiness. 🌈 "],
    "empty":      ["You are not alone — I'm here with you. 🌻 ",
                   "Every small step forward counts! 🚶 "],
    "anxiety":    ["You're stronger than this worry. Take it one step at a time. 💙 ",
                   "I'm here to support you through this. You've got this! 🌟 "],
    "neutral":    ["Here's a little sunshine for your day! ☀️ ",
                   "Hope this brings a smile! 😊 "],
    "fun":        ["Love that energy! 🎉 ", "Let's keep the good vibes going! 🥳 "],
    "surprise":   ["Oh wow, life is full of surprises! 🎊 "],
    "enthusiasm": ["That enthusiasm is contagious! 🔥 "],
    "happiness":  ["So happy to hear that! 😄 ", "Keep shining! ✨ "],
    "love":       ["Love is beautiful! 💕 "],
    "relief":     ["So glad things are looking up! 🌤️ "],
}

def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(csv_path: str | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            User_Input       TEXT NOT NULL,
            Cheerful_Response TEXT NOT NULL,
            Category         TEXT NOT NULL,
            score            REAL DEFAULT 0.0,
            approved         INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM cases")
    if cur.fetchone()[0] == 0 and csv_path and os.path.exists(csv_path):
        print("Seeding database from CSV (first 3 000 rows per emotion)…")
        _seed_from_csv(conn, csv_path, limit_per_emotion=3000)
        print("Database ready ✓")
    conn.close()


def _seed_from_csv(conn: sqlite3.Connection, csv_path: str,
                   limit_per_emotion: int = 3000) -> None:
    counts: dict[str, int] = {}
    rows_to_insert = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emotion = row["emotion"].strip().lower()
            text    = row["text"].strip()
            if not text:
                continue
            counts[emotion] = counts.get(emotion, 0)
            if counts[emotion] >= limit_per_emotion:
                continue
            counts[emotion] += 1
            prefix   = random.choice(CHEERFUL_PREFIXES.get(emotion, ["Here for you! 💙 "]))
            response = prefix + text
            rows_to_insert.append((text, response, emotion))

    conn.executemany(
        "INSERT INTO cases (User_Input, Cheerful_Response, Category) VALUES (?,?,?)",
        rows_to_insert,
    )
    conn.commit()
    print(f"  Inserted {len(rows_to_insert):,} cases across {len(counts)} emotions.")


def get_all_cases() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM cases").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_case(user_input: str, cheerful_response: str, category: str) -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO cases (User_Input, Cheerful_Response, Category, approved) VALUES (?,?,?,1)",
        (user_input, cheerful_response, category),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def mark_approved(case_id: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE cases SET approved=1 WHERE id=?", (case_id,))
    conn.commit()
    conn.close()


def search_cases_by_category(category: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM cases WHERE Category=?", (category,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "emotion_dataset_kaggle.csv")
    init_db(csv_path)
    total = len(get_all_cases())
    print(f"Total cases in DB: {total:,}")
