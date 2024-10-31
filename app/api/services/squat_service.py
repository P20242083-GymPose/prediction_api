from app.api.utils.mediapipe_utils import process_video
from app.api.services import squat_model
import numpy as np
from ...logger import log
def get_score_squat(video):
    """Get the squat score for the given video."""
    try:
        # Process the video for inference
        landmarks = process_video(video)
        input_data = np.expand_dims(landmarks, axis=0)
        score = squat_model.predict(input_data)
        log(f'Squat score: {score[0][0]}', level='INFO')
        return score[0][0], 200
    except Exception as e:
        return str(e), 500