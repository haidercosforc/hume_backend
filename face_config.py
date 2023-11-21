from hume import HumeBatchClient
client = HumeBatchClient("ANojVPFTmCCMyR73Z2ZsLRiTOLlFQpcehCRbBfGaAw6avtAm")

COMPLETED = "COMPLETED"
FAILED = "FAILED"
IN_PROGRESS = "IN_PROGRESS"
QUEUED = "QUEUED"


def facial_emotions(id):
    # id = '638ef96b-99c7-4a0e-8bf9-18dc2bcfe8e5'
    # id = 'f9e129ff-87d8-4e13-944a-56b83c0521d4'

    check = True
    while check:
        details = client.get_job_details(id)
        status = details.state.status.value
        if status.lower() == "completed":
            check = False
        
        elif status == FAILED:
            return {"status": FAILED}

    if check == False:
        predictions = client.get_job_predictions(id)   # The job id will be produced by the Hume model
                                    
        preds = predictions[0]['results']['predictions']

        if 'face' not in preds[0]['models']:
            return {"error": 'No face found'}
        
        model = preds[0]['models']['face'] 
        if len(model['grouped_predictions']) == 0:
            return {"error": "no face detected"}
        
        chunks = model['grouped_predictions'][0]['predictions']
        individuals = len(model['grouped_predictions'])

        total_scores = {}
        for i in range(len(chunks)):
            emotions = chunks[i]['emotions']
            for entity in emotions:
                score = entity['score']
                if score > 0.0:
                    total_scores[entity['name']] = score

        emotions = ['Joy', 'Excitement', 'Satisfaction', 'Pride', 'Contentment',
                    'Interest', 'Romance', 'Surprise (positive)', 'Love']   # list of all of the positive emotions to choose from

        max_emotion = max(total_scores, key=total_scores.get)   # emotion with the heighest intensity
        # After getting the max score we will be setting the 
       
       # all of the emotions apart from the list of the positive emotions required to show the user
        remaining_emotions = {}
        for i in total_scores:
            if i != max_emotion:
                remaining_emotions[i] = total_scores[i]

        max_remianing_emotion = max(remaining_emotions, key=remaining_emotions.get)

        max_score = total_scores[max_emotion]
        remaining_max_score = remaining_emotions[max_remianing_emotion]

        sorted_items = sorted(remaining_emotions.items(), key=lambda x: x[1], reverse=True)

        # Get the top 2 items
        top2_items = sorted_items[:2]

        third_item = top2_items[-1]
        third_emotion = third_item[0]
        third_score = third_item[-1]
        remaining_max_score = (1 - max_score)/2 + 0.03
        third_score = (1 - max_score)/2 - 0.03

        return {"status": COMPLETED,
            "data": [
                {
                "type": max_emotion,
                "score": max_score
                },
                {
                "type": max_remianing_emotion,
                "score": remaining_max_score
                },
                {
                    "type":third_emotion,
                    "score":third_score
                },
            ],
            
            "num_faces": individuals
            }

if __name__ == "__main__":
    face_em = facial_emotions("bcd835ff-8b36-40e8-a150-285b8c91f815")
    a = 0