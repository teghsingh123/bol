import sqlite3

conn = sqlite3.connect("bol.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    artist TEXT,
    year INTEGER,
    lyrics TEXT,
    corrected INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    ) 
""")
conn.commit()
conn.close()

def save_track(title, artist, year, lyrics):
    conn = sqlite3.connect("bol.db")
    cursor = conn.cursor()
    new_track = (title, artist, year, lyrics)
    cursor.execute("INSERT INTO tracks (title, artist, year, lyrics) VALUES (?, ?, ?, ?)", new_track)
    conn.commit()
    conn.close()