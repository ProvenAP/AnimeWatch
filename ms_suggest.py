from flask import Flask, jsonify
import random

app = Flask(__name__)

suggestions = [
    "Attack on Titan",
    "One Piece",
    "Jujutsu Kaisen",
    "Naruto Shippuden",
    "Demon Slayer",
    "Fullmetal Alchemist Brotherhood"
]

@app.route("/suggest", methods=["GET"])
def suggest():
    return jsonify({"suggestion": random.choice(suggestions)})

if __name__ == "__main__":
    app.run(port=5002)
