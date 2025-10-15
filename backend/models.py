import sqlite3
from contextlib import closing
import os

DB_PATH = "fitness.db"

def init_db():
    """Initialize the SQLite database and create the profile table if it doesn’t exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if "/" in DB_PATH else None
    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL,
            activity_level TEXT,
            dietary_pref TEXT,
            allergies TEXT,
            budget TEXT,
            region TEXT,
            goals TEXT
        )
        """)
        con.commit()

def save_profile(data):
    """Save or replace the user's profile information."""
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        # Keep only one user profile (replace existing)
        cur.execute("DELETE FROM profile")
        cur.execute("""
            INSERT INTO profile (
                name, age, gender, height_cm, weight_kg,
                activity_level, dietary_pref, allergies,
                budget, region, goals
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"),
            data.get("age"),
            data.get("gender"),
            data.get("height_cm"),
            data.get("weight_kg"),
            data.get("activity_level"),
            data.get("dietary_pref"),
            data.get("allergies"),
            data.get("budget"),
            data.get("region"),
            data.get("goals")
        ))
        con.commit()

def get_profile():
    """Retrieve the stored user profile, if available."""
    if not os.path.exists(DB_PATH):
        return None
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM profile LIMIT 1")
        row = cur.fetchone()
        if not row:
            return None
        keys = [
            "id", "name", "age", "gender", "height_cm", "weight_kg",
            "activity_level", "dietary_pref", "allergies", "budget", "region", "goals"
        ]
        return dict(zip(keys, row))
