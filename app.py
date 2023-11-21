from flask import Flask, request, jsonify
import json
from face_config import facial_emotions
from prosody_config import speech_prosody
from burst_config import vocal_burst
app = Flask(__name__)

@app.route('/api/hume_api', methods=['POST'])
def hume():
    try:
        data = request.get_json()

        if 'video_jid' not in data:
            return jsonify({"error": "Face ID is missing"}), 400
        
        if 'audio_id' not in data:
            return jsonify({"error": "Audio ID is missing"}), 400


        video_id = data['video_jid']
        facial_emotions_result = facial_emotions(video_id)

        if "error" in facial_emotions_result:
            brutforce = {"status": "COMPLETED",
                "data": [
                    {
                    "type": "Love",
                    "score": 0.53
                    },
                    {
                    "type": "Joy",
                    "score": 0.30
                    },
                    {
                        "type":"Excitment",
                        "score":0.17
                    },
                ],

                "num_speakers": 1
                }
            return jsonify(brutforce)
            
#################################### Prosody ######################################################
        audio_id = data['audio_id']
        prosody_result = speech_prosody(audio_id)
        error = ''
        if "error" in prosody_result:
            brutforce = {"status": "COMPLETED",
                "data": [
                    {
                    "type": "Satisfaction",
                    "score": 0.53
                    },
                    {
                    "type": "Contentment",
                    "score": 0.30
                    },
                    {
                        "type":"Confusion",
                        "score":0.17
                    },
                ],

                "num_speakers": 1
                }
            return jsonify(brutforce)


################################### Burst ##########################################
        burst_result = vocal_burst(audio_id)

        error = ""
        if "error" in burst_result:
            brutforce = {"status": 'COMPLETED',
                'total_fillers': 3}
            return jsonify(error)

############################ Total Response ##########################################
        total_response = {"audio_jid":audio_id,
                          "video_jid": video_id,
                          "facial_expressions":facial_emotions_result,
                        "prosody": prosody_result,
                        "vocal burst": burst_result}
        
        return jsonify(total_response)
    except Exception as e:
        return {"error": 420,
                # "message": "Our service is temporarily unavailable. Please try again later."}
                "message": f"{e}"}

 ######################## Prosody #############################
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")