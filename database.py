"""
database.py
------------
Sets up a SQLite database that persists every prediction the system
makes. This gives the application real, stateful backend behaviour —
predictions are not just computed and discarded, they are logged and
can be reviewed later on the History page.
"""

import sqlite3
from datetime import datetime

DB_PATH = 'predictions.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            tenth_percent REAL NOT NULL,
            twelfth_percent REAL NOT NULL,
            entrance_score REAL NOT NULL,
            category TEXT NOT NULL,
            previous_year_cutoff REAL NOT NULL,
            probability REAL NOT NULL,
            prediction TEXT NOT NULL,
            top_factor TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database 'predictions.db' ready.")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def log_prediction(record):
    """Inserts a single prediction record into the database."""
    conn = get_connection()
    conn.execute('''
        INSERT INTO predictions
        (created_at, tenth_percent, twelfth_percent, entrance_score, category,
         previous_year_cutoff, probability, prediction, top_factor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        record['tenth_percent'], record['twelfth_percent'], record['entrance_score'],
        record['category'], record['previous_year_cutoff'],
        record['probability'], record['prediction'], record['top_factor']
    ))
    conn.commit()
    conn.close()


def get_recent_predictions(limit=25):
    """Returns the most recent prediction records, newest first."""
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM predictions ORDER BY id DESC LIMIT ?', (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary_stats():
    """Returns aggregate stats used on the dashboard."""
    conn = get_connection()
    total = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    avg_prob = conn.execute('SELECT AVG(probability) FROM predictions').fetchone()[0]
    high_chance = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = 'High Chance'"
    ).fetchone()[0]
    conn.close()
    return {
        'total_predictions': total,
        'average_probability': round(avg_prob, 2) if avg_prob else 0,
        'high_chance_count': high_chance
    }


if __name__ == '__main__':
    init_db()
