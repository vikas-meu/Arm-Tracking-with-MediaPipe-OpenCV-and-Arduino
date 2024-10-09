import cv2
import mediapipe as mp
import numpy as np
import pyfirmata

# Initialize Mediapipe Pose Detector
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Initialize Video Capture
cap = cv2.VideoCapture(0)  # 0 is usually the default camera. Change to 1 or 2 if needed.
ws, hs = 1280, 720  # Set the width and height of the frame
cap.set(3, ws)  # Set width
cap.set(4, hs)  # Set height

if not cap.isOpened():
    print("Error: Camera not found or unable to open.")
    exit()

# Initialize Arduino
port = "/dev/ttyACM0"  # Adjust this port based on your setup
try:
    board = pyfirmata.Arduino(port)
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Initialize Servo Pins
servo_pin_shoulder = board.get_pin('d:9:s')   # Servo motor for shoulder joint
servo_pin_elbow = board.get_pin('d:10:s')     # Servo motor for elbow joint
servo_pin_wrist = board.get_pin('d:11:s')     # Servo motor for wrist joint
servo_pin_hand = board.get_pin('d:12:s')      # Servo motor for hand joint

def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between three points using vector mathematics.
    """
    a = np.array(point1)
    b = np.array(point2)
    c = np.array(point3)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    img = cv2.flip(img, 1)  # Flip image horizontally
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = pose.process(img_rgb)  # Process the frame for pose detection
    img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)  # Convert back to BGR

    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_draw.DrawingSpec(color=(0, 255, 255), thickness=4, circle_radius=7),
                               mp_draw.DrawingSpec(color=(0, 0, 0), thickness=4))

        landmarks = results.pose_landmarks.landmark

        # Left arm landmarks: shoulder, elbow, and wrist
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * ws,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * hs]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * ws,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * hs]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * ws,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * hs]
        left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x * ws,
                     landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y * hs]

        # Calculate angles between joints
        shoulder_angle = calculate_angle(left_elbow, left_shoulder, [left_shoulder[0], left_shoulder[1] - 100])  # Vertical reference
        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        wrist_angle = calculate_angle(left_elbow, left_wrist, left_hand)

        # Map angles to servo positions
        servo_shoulder = int(np.interp(shoulder_angle, [0, 180], [0, 180]))
        servo_elbow = int(np.interp(elbow_angle, [0, 180], [0, 180]))
        servo_wrist = int(np.interp(wrist_angle, [0, 180], [0, 180]))

        # Write angles to the servos
        servo_pin_shoulder.write(servo_shoulder)
        servo_pin_elbow.write(servo_elbow)
        servo_pin_wrist.write(servo_wrist)

        # Display angles on screen
        cv2.putText(img, f'Shoulder Angle: {int(shoulder_angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, f'Elbow Angle: {int(elbow_angle)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, f'Wrist Angle: {int(wrist_angle)}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Arm Tracking", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
