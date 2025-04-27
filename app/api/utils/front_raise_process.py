import cv2
import mediapipe as mp
from tensorflow.keras.preprocessing.sequence import pad_sequences

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5)

connections = [
    # Torso connections
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
    
    # Left arm connections
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
    
    # Right arm connections
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST)
]

def extract_landmarks_from_frame(frame):
    """Extracts MediaPipe landmarks for the given frame and returns them as a row of data."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        row = []
        
        for connection in connections:
            start_landmark = landmarks[connection[0].value]
            end_landmark = landmarks[connection[1].value]

            start_x = start_landmark.x * frame.shape[1]
            start_y = start_landmark.y * frame.shape[0]
            end_x = end_landmark.x * frame.shape[1]
            end_y = end_landmark.y * frame.shape[0]

            row.extend([start_x, start_y, end_x, end_y])

        assert len(row) == 32, f"Expected 32 features, but got {len(row)}"
        return row
    else:
        return None 

def process_video_for_inference(video_path, max_sequence_length=70):
    """Extract landmarks from all frames in a video, pad the sequence, and prepare for model input."""
    cap = cv2.VideoCapture(video_path)
    all_landmarks = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        landmarks_row = extract_landmarks_from_frame(frame)

        if landmarks_row is not None:
            all_landmarks.append(landmarks_row)

    cap.release()

    all_landmarks_padded = pad_sequences(all_landmarks, maxlen=max_sequence_length, padding='post', dtype='float32')

    return all_landmarks_padded


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    data = []

    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break


            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                row = [frame_count]

                for connection in connections:
                    start_landmark = landmarks[connection[0].value]
                    end_landmark = landmarks[connection[1].value]

                    start_x = int(start_landmark.x * frame.shape[1])
                    start_y = int(start_landmark.y * frame.shape[0])
                    end_x = int(end_landmark.x * frame.shape[1])
                    end_y = int(end_landmark.y * frame.shape[0])

                    row.extend([start_x, start_y, end_x, end_y])

                data.append(row)

            frame_count += 1

    cap.release()

    return data