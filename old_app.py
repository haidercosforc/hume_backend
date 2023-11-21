from flask import Flask, request, jsonify
import json
from face_config import facial_emotions
from prosody_config import speech_prosody
from burst_config import vocal_burst
app = Flask(__name__)

@app.route('/api/facial_expression', methods=['POST'])
def facial_expression():
    data = request.get_json()

    if 'id' not in data:
        return jsonify({"error": "ID is missing"}), 400

    id_str = data['id']
    result = facial_emotions(id_str)

    if "error" in result:
        if result['error'] == "No face found":
            return {"error": 444,
                    "message": "hume's facial expression model didnt respond"}
    
    if "error" in result:
        if result['error'] == "no face detected":
            return {'error': 445,
                    "message": "couldn't detect facial expressions"}

    return jsonify(result)


@app.route('/api/prosody', methods=['POST'])
def prosody():
    data = request.get_json()

    if 'id' not in data:
        return jsonify({"error": "ID is missing"}), 400

    id_str = data['id']
    result = speech_prosody(id_str)

    if "error" in result:
        if result["error"] == "No prosody found":
            return {"error": 444,
                    "message": "hume's prosody model didn't respond"}
        
        elif result['error'] == 'emotions not detected':
            return {'error': 445,
                    "message": "couldn't understand the speech"}

    return jsonify(result)


@app.route('/api/burst', methods=['POST'])
def burst():
    data = request.get_json()

    if 'id' not in data:
        return jsonify({"error": "ID is missing"}), 400

    id_str = data['id']
    result = vocal_burst(id_str)

    if "error" in result:
        if result['error'] == "No burst found":
            return {"error": 444}

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # id = "92dfebc1-00f3-4244-ae1b-42ea4d524671"
    # get_prosody = facial_emotions(id)

    # a = 7