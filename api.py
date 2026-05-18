from flask import Flask, request, jsonify
from flask_cors import CORS
from database import save_track

app = Flask(__name__)
CORS(app)

@app.route("/save", methods=["POST"]) #type: ignore
def save():
    data = request.get_json()
    save_track(data["title"], data["artist"], data["year"], data["lyrics"])
    return jsonify({"status": "ok"})
if __name__ == "__main__":
    app.run(debug=True)