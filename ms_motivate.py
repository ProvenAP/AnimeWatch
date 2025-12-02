from flask import Flask, jsonify
import random

app = Flask(__name__)

quotes = [
    "Keep going — you’re closer than you think.",
    "Progress is progress, even if it's slow.",
    "Small steps still move you forward.",
    "Consistency beats motivation every time.",
    "You only fail if you stop trying."
]

@app.route("/motivate", methods=["GET"])
def motivate():
    return jsonify({"quote": random.choice(quotes)})

if __name__ == "__main__":
    app.run(port=5004)
