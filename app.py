import cv2
import mediapipe as mp
import time
import random
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
feedback_messages = {
    'good_posture': [
        'Great job! Keep maintaining that good posture.',
        'Your posture looks excellent. Keep it up!',
        'You have good posture. Stay consistent!',
        'Nice! Your back is straight and aligned.'
    ],
    'improve_posture': [
        'Please keep your back straight!',
        'Adjust your posture to straighten your back.',
        'It looks like you’re slouching. Sit up straight!',
        'Improve your posture by aligning your shoulders.'
    ],
    'adjust_position': [
        'Please adjust your position for better posture detection.',
        'Make sure you are clearly visible in the frame.',
        'Reposition yourself so the system can detect your posture.'
    ]
}

def get_random_message(message_type):
    messages = feedback_messages[message_type]
    return random.choice(messages)
cap = cv2.VideoCapture(0)

current_feedback = ''
last_feedback_time = 0
feedback_interval = 7  

while cap.isOpened():
    ret, frame = cap.read
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        current_time = time.time()
        if current_time - last_feedback_time > feedback_interval:
            if (left_shoulder.visibility > 0.5 and right_shoulder.visibility > 0.5 and 
                left_hip.visibility > 0.5 and right_hip.visibility > 0.5):
                
                shoulder_slope = abs(left_shoulder.y - right_shoulder.y)
                hip_slope = abs(left_hip.y - right_hip.y)

                if shoulder_slope > 0.05 or hip_slope > 0.05:
                    current_feedback = get_random_message('improve_posture')
                else:
                    current_feedback = get_random_message('good_posture')
            else:
                current_feedback = get_random_message('adjust_position')

            print(current_feedback)
            last_feedback_time = current_time

    # Display the frame
    cv2.imshow('Posture Correction', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
