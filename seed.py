import sqlite3

conn = sqlite3.connect('bol.db')
cursor = conn.cursor()


# insert test tracks linked to album 1 (Nasha)
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 1', 'Babbu Maan', 2001, 1)")
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 2', 'Babbu Maan', 2001, 1)")
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 3', 'Babbu Maan', 2001, 1)")

# insert test tracks linked to album 2 (Pyaas)
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 4', 'Babbu Maan', 2004, 2)")
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 5', 'Babbu Maan', 2004, 2)")

# insert test tracks linked to album 3 (Saun Di Jhadi)
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 6', 'Harbhajan Mann', 1999, 3)")
cursor.execute("INSERT INTO tracks (title, artist, year, album_id) VALUES ('Track 7', 'Harbhajan Mann', 1999, 3)")


conn.commit()
conn.close()
print('done')