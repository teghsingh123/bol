from flask import Flask, request, jsonify
from flask_cors import CORS
from database import save_track, save_album

import sqlite3

app = Flask(__name__)
CORS(app)

#save a track to the database
@app.route("/save", methods=["POST"])
def handle_save_track():
    data = request.get_json()
    save_track(data["title"], data["artist"], data["year"], data["lyrics"])
    return jsonify({"status": "ok"})

#save an album to the database
@app.route("/save_album", methods=["POST"])
def handle_save_album():
    data = request.get_json()
    save_album(data["title"], data["artist"], data["year"], data["cover_image"])
    return jsonify({"status": "ok"})

#show all albums
@app.route("/albums", methods=["GET"])
def handle_albums():
    conn = sqlite3.connect("bol.db")
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM albums").fetchall()
    conn.close()
    albums = []
    for row in rows:
        album_dict = {"id": row[0], "title": row[1], "artist": row[2], "year": row[3], "cover_image": row[4]}
        albums.append(album_dict)
    return jsonify(albums)

#showcase all tracks of a given album id
@app.route("/albums/<id>/tracks", methods=["GET"])
def handle_tracks(id):
    conn = sqlite3.connect("bol.db")
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM tracks WHERE album_id = ?", (id,)).fetchall()
    conn.close()
    tracks = []
    for row in rows:
        track_dict = {"id": row[0], "title": row[1], "artist": row[2], "year": row[3], "lyrics": row[4]}
        tracks.append(track_dict)
    return jsonify(tracks)







if __name__ == "__main__":
    app.run(debug=True)