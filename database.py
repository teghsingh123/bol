import sqlite3

conn = sqlite3.connect("bol.db")
cursor = conn.cursor()

#tracks
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    artist TEXT,
    year INTEGER,
    lyrics TEXT,
    corrected INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    album_id INTEGER
    ) 
""")

#albums
cursor.execute("""
    CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    artist TEXT,
    year INTEGER,
    cover_image TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()

#save a track to tracks
def save_track(title, artist, year, lyrics):
    conn = sqlite3.connect("bol.db")
    cursor = conn.cursor()
    new_track = (title, artist, year, lyrics)
    cursor.execute("INSERT INTO tracks (title, artist, year, lyrics) VALUES (?, ?, ?, ?)", new_track)
    conn.commit()
    conn.close()

#save an album to albums
def save_album(title, artist, year, cover_image):
    conn = sqlite3.connect("bol.db")
    cursor = conn.cursor()
    new_album = (title, artist, year, cover_image)
    cursor.execute("INSERT INTO albums (title, artist, year, cover_image) VALUES (?, ?, ?, ?)", new_album)
    conn.commit()
    conn.close()