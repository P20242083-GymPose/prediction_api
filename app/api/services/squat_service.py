from app.api.utils.squat_process import process_video
from app.api.services import squat_model
import numpy as np
from flask import jsonify
from ...logger import log
def get_score_squat(video):
    """Get the squat score for the given video."""
    try:
        landmarks = process_video(video)
        if not landmarks:
            return jsonify({'error': 'No landmarks found, please provide a clearer video'}), 400
        input_data = np.expand_dims(landmarks, axis=0)
        score = squat_model.predict(input_data)
        log(f'Squat score: {score[0][0]}', level='INFO')
        return score[0][0], 200
    except Exception as e:
        log(f'Error processing squat video: {str(e)}', level='ERROR')
        return str(e), 500