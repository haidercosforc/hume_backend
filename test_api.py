from flask import Flask, request, jsonify
import json
from face_config import facial_emotions
from prosody_config import speech_prosody
from burst_config import vocal_burst

def facial_expression(id):
    try:
        id_str = id
        facial_emotions_result = facial_emotions(id_str)

        error = ""
        if "error" in facial_emotions_result:

            if facial_emotions_result['error'] == "No face found":
                error =  {"error": 444,
                    "message": "hume's facial expression model didn't respond"}
        
            elif facial_emotions_result['error'] == "no face detected":
                error = {'error': 445,
                        "message": "couldn't detect facial expressions"}

            
            facial_emotions_result = {"status": "FAILED",
            "data": [
                {
                "type": "",
                "score": ""
                },
                {
                "type": "",
                "score": ""
                },
                {
                    "type":"",
                    "score":""
                },
            ],
            
            "num_faces": ""
            }

        facial_data = {"response":facial_emotions_result, 
                    "error_message": error}

    ##################### Prosody ##############################
        prosody_result = speech_prosody(id_str)
        error = ''
        if "error" in prosody_result:
            if prosody_result["error"] == "No prosody found":
                error = {"error": 444,
                        "message": "hume's prosody model didn't respond"}
            
            elif prosody_result['error'] == 'emotions not detected':
                error = {'error': 445,
                        "message": "couldn't understand the speech"}
            
            prosody_result = {"status": "FAILED",
                "data": [
                    {
                    "type": "",
                    "score": ""
                    },
                    {
                    "type": "",
                    "score": ""
                    },
                    {
                        "type":"",
                        "score":""
                    },
                ],

                "num_speakers": ""
                }

        prosody_data = {"response": prosody_result, "error_message": error}


################################### Burst ##########################################
        burst_result = vocal_burst(id_str)

        error = ""
        if "error" in burst_result:
            
            if burst_result['error'] == "No burst found":
                error = {"error": 444}

            burst_result = {"status": "FAILED",
                    'total_fillers': ""}
            
        burst_data = {"response": burst_result,
                    "error_message": error}

############################ Total Response ##########################################
        total_response = {"facial_expressions": facial_data,
                        "prosody": prosody_data,
                        "vocal burst": burst_data}
        
        return jsonify(total_response)
    except Exception as e:
        return {"error": 420,
                "message": e}
#    
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    # id = "92dfebc1-00f3-4244-ae1b-42ea4d524671"
    # get_prosody = facial_emotions(id)
    total_jid = "29c804d4-6cc5-4fa4-924b-cd8229243d70"
    facial_expression(total_jid)
    a = 7