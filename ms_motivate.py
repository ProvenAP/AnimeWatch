from flask import Flask
import random

app = Flask(__name__)

lines = [
    "keep going, you're doing great!",
    "small steps still move forward.",
    "you got this—don’t give up now!"
]

@app.route("/motivate")
def motivate():
    return random.choice(lines)

if __name__ == "__main__":
    app.run(port=5003)
