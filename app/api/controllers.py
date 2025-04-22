from flask import request, jsonify
import os
from app.api.blueprint import blueprint
from app.api.services.squat_service import get_score_squat as calculate_squat_score
from app.api.services.bicep_curl_service import get_score_bicep_curl as calculate_bicep_curl_score
from app.api.services.front_raise_service import get_score_front_raise as calculate_front_raise_score
# Define the fixed path for the video file
VIDEO_FILE_PATH = 'app/uploads/videos/latest_squat_video.mp4'
os.makedirs(os.path.dirname(VIDEO_FILE_PATH), exist_ok=True)  # Ensure directory exists



@blueprint.route('/get-score-squat', methods=['POST'])
def get_score_squat_route():
    try:
        #check for video file in the
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video = request.files['video']
        
        # Save the file with a fixed name, overwriting any previous file
        video.save(VIDEO_FILE_PATH)
        
        # Pass the saved video file path to the squat scoring service
        score, status = calculate_squat_score(VIDEO_FILE_PATH)
        
        # Return the score
        return jsonify({'score': str(score)}), status
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blueprint.route('/get-score-bicep-curl', methods=['POST'])
def get_score_squat_route():
    try:
        #check for video file in the
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video = request.files['video']
        
        # Save the file with a fixed name, overwriting any previous file
        video.save(VIDEO_FILE_PATH)
        
        # Pass the saved video file path to the squat scoring service
        score, status = calculate_bicep_curl_score(VIDEO_FILE_PATH)
        
        # Return the score
        return jsonify({'score': str(score)}), status
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@blueprint.route('/get-score-front-raise', methods=['POST'])
def get_score_squat_route():
    try:
        #check for video file in the
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video = request.files['video']
        
        # Save the file with a fixed name, overwriting any previous file
        video.save(VIDEO_FILE_PATH)
        
        # Pass the saved video file path to the squat scoring service
        score, status = calculate_front_raise_score(VIDEO_FILE_PATH)
        
        # Return the score
        return jsonify({'score': str(score)}), status
    except Exception as e:
        return jsonify({'error': str(e)}), 500