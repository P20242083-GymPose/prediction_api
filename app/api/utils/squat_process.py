import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5)

# Specify connections to extract
connections = [
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP)
]

# Extract landmarks from a frame
def extract_landmarks_from_frame(frame):
    """Extracts MediaPipe landmarks for the given frame and returns them as a row of data."""
    # Convert the frame to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # If landmarks are detected, extract and return them
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        row = []
        
        # Extract coordinates for each connection
        for connection in connections:
            start_landmark = landmarks[connection[0].value]
            end_landmark = landmarks[connection[1].value]

            # Get coordinates and scale them to the frame dimensions
            start_x = start_landmark.x * frame.shape[1]
            start_y = start_landmark.y * frame.shape[0]
            end_x = end_landmark.x * frame.shape[1]
            end_y = end_landmark.y * frame.shape[0]

            # Append the coordinates to the row (flattened)
            row.extend([start_x, start_y, end_x, end_y])

        # Ensure row length matches the expected number of features (32 features)
        assert len(row) == 32, f"Expected 32 features, but got {len(row)}"
        return row
    else:
        return None  # Return None if no landmarks are detected

# Process a single video for inference
def process_video_for_inference(video_path, max_sequence_length=70):
    """Extract landmarks from all frames in a video, pad the sequence, and prepare for model input."""
    cap = cv2.VideoCapture(video_path)
    all_landmarks = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Extract landmarks for the current frame
        landmarks_row = extract_landmarks_from_frame(frame)

        if landmarks_row is not None:
            all_landmarks.append(landmarks_row)

    cap.release()

    # Ensure all sequences have the same length by padding shorter ones
    all_landmarks_padded = pad_sequences(all_landmarks, maxlen=max_sequence_length, padding='post', dtype='float32')

    return all_landmarks_padded


def process_video(video_path):
    # Start video capture from file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    # Initialize a list to store the data
    data = []

    # Initialize the Pose module
    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break


            # Convert the image to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image and find pose landmarks
            results = pose.process(image_rgb)

            # If landmarks are detected
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Prepare a row to store the coordinates
                row = [frame_count]

                # Draw and store the coordinates for each specified connection
                for connection in connections:
                    start_landmark = landmarks[connection[0].value]
                    end_landmark = landmarks[connection[1].value]

                    # Get the coordinates
                    start_x = int(start_landmark.x * frame.shape[1])
                    start_y = int(start_landmark.y * frame.shape[0])
                    end_x = int(end_landmark.x * frame.shape[1])
                    end_y = int(end_landmark.y * frame.shape[0])

                    # Append the coordinates to the row
                    row.extend([start_x, start_y, end_x, end_y])

                # Append the row to the data list
                data.append(row)

            frame_count += 1

    # Release the video capture
    cap.release()

    return data