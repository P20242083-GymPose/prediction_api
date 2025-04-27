from app.api.utils.front_raise_process import process_video
from app.api.services import front_raise_model
import numpy as np
from ...logger import log
def get_score_front_raise(video):
    """Get the front raise score for the given video."""
    try:
        # Process the video for inference
        landmarks = process_video(video)
        if not landmarks:
            return "No valid frames detected. Video too short or no pose detected.", 400
        input_data = np.expand_dims(landmarks, axis=0)
        score = front_raise_model.predict(input_data)
        log(f'Front raise score: {score[0][0]}', level='INFO')
        return score[0][0], 200
    except Exception as e:
        log(f'Error processing front raise video: {str(e)}', level='ERROR')
        return str(e), 500