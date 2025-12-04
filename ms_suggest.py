from flask import Flask
import random

app = Flask(__name__)

suggestions = [
    "try watching Demon Slayer next.",
    "you might like Jujutsu Kaisen.",
    "give Vinland Saga a shot!"
]

@app.route("/suggest")
def suggest():
    return random.choice(suggestions)

if __name__ == "__main__":
    app.run(port=5004)
