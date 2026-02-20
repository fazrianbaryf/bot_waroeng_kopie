import sqlite3

DB_FILE = "database.db"

def setup():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_points(user_id, points):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, points) VALUES (?, ?)", (user_id, points))
    conn.commit()
    conn.close()

def get_points(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, points FROM users ORDER BY points DESC LIMIT 10")
    result = cursor.fetchall()
    conn.close()
    return result
