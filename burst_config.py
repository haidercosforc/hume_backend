from hume import HumeBatchClient
client = HumeBatchClient("ANojVPFTmCCMyR73Z2ZsLRiTOLlFQpcehCRbBfGaAw6avtAm")

COMPLETED = "COMPLETED"
FAILED = "FAILED"
IN_PROGRESS = "IN_PROGRESS"
QUEUED = "QUEUED"


def vocal_burst(id):
    client = HumeBatchClient("ANojVPFTmCCMyR73Z2ZsLRiTOLlFQpcehCRbBfGaAw6avtAm")

    check = True
    while check:
        details = client.get_job_details(id)
        status = details.state.status.value
        if status.lower() == "completed":
            check = False

        elif status == FAILED:
            return {"status": FAILED}
    
    
    if check==False:
        predictions = client.get_job_predictions(id)   # The job id will be produced by the Hume model                       
        preds = predictions[0]['results']['predictions']
        
        if 'burst' not in preds[0]['models']:
            return {'error': 'No burst found'}
        
        model = preds[0]['models']['burst'] # only concerened with the prosody model

        if len(model['grouped_predictions']) == 0:
            return {'total_fillers': 0}
        
        else:
            chunks = model['grouped_predictions'][0]['predictions']

            total_emotions = []
            total_scores = {}
            for i in range(len(chunks)):
                emotions = chunks[i]['descriptions']
                for entity in emotions:
                    score = entity['score']
                    if score > 0.2:         #any emotion with less thatn 20% probability
                        total_emotions.append(entity['name'])
                        
            return {"status": COMPLETED,
                    'total_fillers': len(total_emotions)}