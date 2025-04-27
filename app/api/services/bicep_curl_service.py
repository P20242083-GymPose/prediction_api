from app.api.utils.bicep_process import process_video
from app.api.services import bicep_curl_model
import numpy as np
from ...logger import log
from flask import jsonify
def get_score_bicep_curl(video):
    """Get the bicep curl score for the given video."""
    try:
        # Process the video for inference
        landmarks = process_video(video)
        if not landmarks:
            return jsonify({'error': 'No landmarks found, please provide a clearer video'}), 400
        input_data = np.expand_dims(landmarks, axis=0)
        score = bicep_curl_model.predict(input_data)
        log(f'Bicep curl score: {score[0][0]}', level='INFO')
        return score[0][0], 200
    except Exception as e:
        log(f'Error processing bicep curl video: {str(e)}', level='ERROR')
        return str(e), 500