from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/time", methods=["GET"])
def get_time():
    return jsonify({"timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(port=5001)
