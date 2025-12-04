from flask import Flask
import random

app = Flask(__name__)

facts = [
    "Naruto was originally supposed to be a chef.",
    "One Piece is the best-selling manga ever.",
    "Attack on Titan took 11 years to complete.",
    "Luffy was almost designed to have black hair.",
    "The first anime ever made was in 1917."
]

@app.route("/fact")
def fact():
    return random.choice(facts)

if __name__ == "__main__":
    app.run(port=5002)
