from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.get("/time")
def get_time():
    now = datetime.now()
    nice = now.strftime("%B %d, %Y – %I:%M %p")
    return nice

if __name__ == "__main__":
    print("➡️  Time microservice running on port 5001")
    app.run(port=5001)
