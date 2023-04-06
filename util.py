# Imports
import cv2
import math
import mediapipe as mp
from pose_logger import logger
import os

# Build Keypoints using MP Holistic
mp_holistic = mp.solutions.holistic      # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

if os.path.exists("ArmyPose.log"):
    os.remove("ArmyPose.log")
    #create a file
    f = open("ArmyPose.log", "w")
    f.close()

window_size = (0, 0)

def get_name_of_user():
    name = input("Enter your name: ")
    # validate name
    while not name.isalpha():
        print("Invalid name. Please enter again (alphabets only).")
        name = input("Enter your name: ")
    return name


def get_id_of_user():
    ID = input("Enter your ID: ")
    # validate ID
    while not ID.isdigit():
        print("Invalid ID. Please enter valid Number.")
        ID = input("Enter your ID: ")
    return ID


def get_activity_name():
    activity_name = input("Enter the name of the activity: ")
    # validate activity name
    while not activity_name.isalpha():
        print("Invalid activity name. Please enter again (alphabets only).")
        activity_name = input("Enter the name of the activity: ")
    return activity_name


def get_user_choice():
    position = ['Savdhan', 'Vishram', 'Baye Salute', 'Daine Salute', 'Front Salute',
                'Khade_Khade_Daine_Mud', 'Khade_Khade_Baye_Mud', 'Khade_Khade_Peeche_Mud']
    print("Choose the position to be checked:")
    print("1. Savdhan")
    print("2. Vishram")
    print("3. Baye Salute")
    print("4. Daine Salute")
    print("5. Front Salute")
    print("6. Khade Khade Daine Mud")
    print("7. Khade Khade Baye Mud")
    print("8. Khade Khade Peeche Mud")

    choice = input("Enter your choice: ")
    # validate choice
    while not choice.isdigit() or int(choice) not in range(1, 9):
        print("Invalid choice. Please enter again [1,8].")
        choice = input("Enter your choice: ")
    return int(choice), position[int(choice) - 1]


def get_angle_between_three_points(landmark1, landmark2, landmark3):
    """
    Returns angle between the two vectors formed by the passed three points
    Input: landmark1, landmark2, landmark3
        landmark1: (x1, y1) in this form
        landmark2 is the joining point
    Output: angle in degrees
    """
    # Get the required landmarks coordinates.
    x1, y1 = landmark1
    x2, y2 = landmark2
    x3, y3 = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    # Check if the angle is less than zero.
    if angle < 0:
        # Add 360 to the found angle.
        angle += 360
    return angle


def get_distance(p, q):
    """
    Return euclidean distance between points p and q
    assuming both to have the same number of dimensions
    """
    # sum of squared difference between coordinates
    s_sq_difference = 0
    for p_i, q_i in zip(p, q):
        s_sq_difference += (p_i - q_i) ** 2

    # take sq root of sum of squared difference
    distance = s_sq_difference ** 0.5
    return distance


def check_direction(landmark1, landmark2):
    x1, y1 = landmark1
    x2, y2 = landmark2
    return x1 - x2


def midpoint(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2) // 2, (y1 + y2) // 2


def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)  # Draw face connections
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(
        image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(
        image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections


def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(color=(80, 110, 10),
                               thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))


def run_mediapipe_holistic(frame):
    with mp_holistic.Holistic(
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3,
        static_image_mode=False
    ) as holistic:  # static_image=True
        image, results = mediapipe_detection(frame, holistic)
        # draw_landmarks(image, results)
        return results, image


def mediapipe_detection(image, model):
    # COLOR CONVERSION BGR 2 RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  # Image is no longer writable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writable
    # COLOR CONVERSION RGB 2 BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

# =============================================================== CHECK POSITIONS ===============================================================

def vishram(results, frame):

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    heel_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    heel_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    # check if body is visible
    if shoulder_right.visibility < 0.7 or \
            shoulder_left.visibility < 0.7 or \
            hip_right.visibility < 0.7 or hip_left.visibility < 0.7 or heel_left.visibility < 0.7 or \
            heel_right.visibility < 0.7 or ear_right.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7 or knee_right.visibility < 0.7:
        cv2.putText(frame, "Entire body not visible", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    heel_left_coordinates = (int(heel_left.x * width),
                             int(heel_left.y * height))
    heel_right_coordinates = (
        int(heel_right.x * width), int(heel_right.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_heels = get_distance(
        heel_left_coordinates, heel_right_coordinates)

    back_posture_check = back_posture > 160 and back_posture < 200
    body_posture_check = body_posture > 160 and body_posture < 200
    distance_between_heels_check = distance_between_heels > 50 and distance_between_heels < 120
    # print(distance_between_heels)
    wrist_visibilty_check = wrist_right.visibility < 0.3 and wrist_left.visibility < 0.3 and elbow_left.visibility < 0.3 and elbow_right.visibility < 0.3
    # print(wrist_left.visibility)

    if back_posture_check and body_posture_check and distance_between_heels_check and wrist_visibilty_check:
        cv2.putText(frame, "Correct Vishram Position",
                    (window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        logger.info("Correct Front Vishram Position")
        return True, frame

    else:
        cv2.putText(frame, "Incorrect Vishram Position",
                    (window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        logger.info("Incorrect Front Savdhan Position")

        # ? These feedbacks are printed at the bottom of screen and hence you might miss them
        # * In future the screen will be responsive to accomodate the video display frame
        if not back_posture_check:
            # print(f'Inside back_posture_check: {back_posture_check}')
            cv2.putText(frame, "Incorrect Back Posture", (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            logger.info("Incorrect back posture")
            logger.info(f'back_posture: {back_posture}: (160, 200)')
        if not body_posture_check:
            # print(f'Inside body_posture_check: {body_posture_check}')
            cv2.putText(frame, "Incorrect Body Posture", (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            logger.info("Incorrect body posture")
            logger.info(f'body_posture: {body_posture}: (160, 200)')  
        if not distance_between_heels_check:
            # print('Inside distance_between_heels_check: {distance_between_heels_check}')
            cv2.putText(frame, "Incorrect Distance between Heels", (
                window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            logger.info(f'Incorrect distance between knees')
            logger.info(f'distance_between_heels: {distance_between_heels}: (50, 120)')
        if not wrist_visibilty_check:
            # print(f'Inside wrist_visibilty_check: {wrist_visibilty_check}')
            cv2.putText(frame, "Wrists should not be visible", (
                window_size[0]-800, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            logger.info(f'Wrists should not be visible')
            logger.info(f'wrist_right.visibility: {wrist_right.visibility}: (< 0.3)')
        return False, frame


def savdhan(results, frame):

    height, width, _ = frame.shape

    # angle between shoulder, elbow and wrist should be around 170 for both hands
    # angle between center of shoulder and center of hip and center of ankle should be around 180
    # angle between center of ear and center of shoulder and center of hip should be around 180
    # distance betweeen wrist and hip should be less (need to find out the exact distance)

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    heel_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    heel_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]
    left_foot_index = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_foot_index = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]

    # check if body is visible
    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_right.visibility < 0.7 or hip_left.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ankle_left.visibility < 0.7 or ear_right.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7 or knee_right.visibility < 0.7:
        cv2.putText(frame, "Entire body not visible", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    heel_left_coordinates = (int(heel_left.x * width),
                             int(heel_left.y * height))
    heel_right_coordinates = (
        int(heel_right.x * width), int(heel_right.y * height))
    left_foot_index_coordinates = (
        int(left_foot_index.x * width), int(left_foot_index.y * height))
    right_foot_index_coordinates = (
        int(right_foot_index.x * width), int(right_foot_index.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ankle_center_coordinates = midpoint(
        ankle_left_coordinates, ankle_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)
    heel_center_coordinates = midpoint(
        heel_left_coordinates, heel_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)
    angle_between_ankle = get_angle_between_three_points(
        left_foot_index_coordinates, heel_center_coordinates, right_foot_index_coordinates)

    distance_between_knees = get_distance(
        knee_left_coordinates, knee_right_coordinates)
    distance_between_ankles = get_distance(
        ankle_left_coordinates, ankle_right_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)

    back_posture_check = back_posture > 160 and back_posture < 210
    body_posture_check = body_posture > 160 and body_posture < 200
    distance_between_knees_check = distance_between_knees > 35 and distance_between_knees < 60
    distance_between_ankles_check = distance_between_ankles > 15 and distance_between_ankles < 45
    distance_between_rightwrist_righthip_check = distance_between_rightwrist_righthip > 30 and distance_between_rightwrist_righthip < 60
    distance_between_leftwrist_lefthip_check = distance_between_leftwrist_lefthip > 30 and distance_between_leftwrist_lefthip < 60
    angle_between_ankle_check = angle_between_ankle > 80 and angle_between_ankle < 120
    # TODO: wrist closure calculation

    if back_posture_check and body_posture_check and distance_between_knees_check and \
        distance_between_ankles_check and distance_between_rightwrist_righthip_check and \
            distance_between_leftwrist_lefthip_check and angle_between_ankle_check:
        cv2.putText(frame, "Correct Front Savdhan Position",
                    (window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        logger.info("Correct Front Savdhan Position")
        return True, frame
    else:
        cv2.putText(frame, "Incorrect Front Savdhan Position",
                    (window_size[0]-800, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        logger.info("Incorrect Front Savdhan Position")

        if not back_posture_check:
            cv2.putText(frame, "Incorrect back posture", (
                window_size[0]-600, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect back posture")
            logger.info(f'back_posture: {back_posture}: (160, 210)')
        if not body_posture_check:
            cv2.putText(frame, "Incorrect body posture", (
                window_size[0]-600, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect body posture")
            logger.info(f'body_posture: {body_posture}: (160, 200)')
        if not distance_between_knees_check:
            cv2.putText(frame, "Put knees close together", (
                window_size[0]-600, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between knees')
            logger.info(f'distance_between_knees: {distance_between_knees}: (35, 60)')
        if not distance_between_ankles_check:
            cv2.putText(frame, "Put ankles close together", (
                window_size[0]-600, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between ankles')
            logger.info(f'distance_between_ankles: {distance_between_ankles}: (15, 45)')
        if not distance_between_rightwrist_righthip_check:
            cv2.putText(frame, "Put left wrist close to left hip", (
                window_size[0]-600, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between rightwrist_righthip')
            logger.info(f'distance_between_rightwrist_righthip: {distance_between_rightwrist_righthip}: (30, 60)')
        if not distance_between_leftwrist_lefthip_check:
            cv2.putText(frame, "Put right wrist close to right hip", (
                window_size[0]-600, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between leftwrist_lefthip')
            logger.info(f'distance_between_leftwrist_lefthip: {distance_between_leftwrist_lefthip}: (30, 60)')
        if not angle_between_ankle_check:
            cv2.putText(frame, "Incorrect angle between ankles", (
                window_size[0]-600, window_size[1]-0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect angle between ankles')
            logger.info(f'angle_between_ankle: {angle_between_ankle}: (80, 120)')
        return False, frame


def savdhan_back(results, frame):
    if results.pose_landmarks is None:
        print("None detected")
    height, width, _ = frame.shape

    # TODO: every position requires different check for visibility
    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_knees = get_distance(
        knee_left_coordinates, knee_right_coordinates)
    distance_between_ankles = get_distance(
        ankle_left_coordinates, ankle_right_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)

    # TODO: how to detect hands are rolled in a box or not
    # CHANGE THESE VALUES to make them more accurate for detection
    # face should not be visible
    if (not results.face_landmarks):
        if (back_posture > 160 and back_posture < 210) and \
                body_posture > 160 and body_posture < 200 and \
                distance_between_knees > 39 and distance_between_knees < 56 and \
                distance_between_ankles > 19 and distance_between_ankles < 36 and \
                distance_between_rightwrist_righthip > 35 and distance_between_rightwrist_righthip < 75 and \
                distance_between_leftwrist_lefthip > 19 and distance_between_leftwrist_lefthip < 66:
            cv2.putText(frame, "Correct Back Savdhan Position", (
                window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return True, frame
        else:
            cv2.putText(frame, "Incorrect Back Savdhan Position", (
                window_size[0]-500, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Back Posture: " + str(back_posture),
                        (window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Body Posture: " + str(body_posture),
                        (window_size[0]-500, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Distance Between Knees: " + str(distance_between_knees),
                        (window_size[0]-500, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Distance Between Ankles: " + str(distance_between_ankles),
                        (window_size[0]-500, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Distance Between Right Wrist and Right Hip: " + str(distance_between_rightwrist_righthip),
                        (window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Distance Between Left Wrist and Left Hip: " + str(distance_between_leftwrist_lefthip),
                        (window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            return False, frame
    else:
        return False, frame


def right_side_savdhan(results, frame):
    # tip of feet - heel of feet > 0 for both feet
    # angle between shoulder, elbow, wrist > 160 and < 190 for both arms
    # distance between shoulder constraint and hip constraint for sideways position

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    # check if body is visible
    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            hip_right.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ear_right.visibility < 0.7 or \
            knee_right.visibility < 0.7:
        cv2.putText(frame, "Face the right side", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    distance_between_rightknee_leftknee = get_distance(
        knee_right_coordinates, knee_left_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)

    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    if distance_left > 0 and distance_right > 0 and \
            back_posture > 158 and back_posture < 195 and \
            body_posture > 170 and body_posture < 190 and \
            distance_between_rightshoulder_leftshoulder < 38 and \
            distance_between_rightknee_leftknee < 25 and \
            distance_between_rightwrist_righthip < 45 and \
            distance_between_leftwrist_lefthip < 25:
        cv2.putText(frame, f'Correct Right Savdhan',
                    (window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame

    else:
        cv2.putText(frame, f'Incorrect Right Savdhan',
                    (window_size[0]-500, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Back Posture: {back_posture}', (
            window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Body Posture: {body_posture}', (
            window_size[0]-500, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right shoulder and left shoulder: {distance_between_rightshoulder_leftshoulder}', (
            window_size[0]-500, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right knee and left knee: {distance_between_rightknee_leftknee}', (
            window_size[0]-500, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right wrist and right hip: {distance_between_rightwrist_righthip}', (
            window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between left wrist and left hip: {distance_between_leftwrist_lefthip}', (
            window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def left_side_savdhan(results, frame):

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    # check if body is visible
    if shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_left.visibility < 0.7 or ankle_left.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7:
        cv2.putText(frame, "Face the left side", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    distance_between_rightknee_leftknee = get_distance(
        knee_right_coordinates, knee_left_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)

    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    if distance_left < 0 and distance_right < 0 and \
            back_posture > 158 and back_posture < 195 and \
            body_posture > 170 and body_posture < 190 and \
            distance_between_rightshoulder_leftshoulder < 38 and \
            distance_between_rightknee_leftknee < 25 and \
            distance_between_rightwrist_righthip < 25 and \
            distance_between_leftwrist_lefthip < 45:
        cv2.putText(frame, f'Correct Left savdhan',
                    (window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame
    else:
        cv2.putText(frame, f'Incorrect Left savdhan',
                    (window_size[0]-500, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Back posture: {back_posture}', (
            window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Body posture: {body_posture}', (
            window_size[0]-500, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right shoulder and left shoulder: {distance_between_rightshoulder_leftshoulder}', (
            window_size[0]-500, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right knee and left knee: {distance_between_rightknee_leftknee}', (
            window_size[0]-500, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right wrist and right hip: {distance_between_rightwrist_righthip}', (
            window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between left wrist and left hip: {distance_between_leftwrist_lefthip}', (
            window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def baye_salute_old(results, frame):
    # initially right side facing
    # salute towards camera
    # hand won't be visible directly

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]
    index_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX]

    height, width, _ = frame.shape

    # check if body is visible
    if shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_left.visibility < 0.7 or ankle_left.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7:
        cv2.putText(frame, "Face the left side", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    index_left_coordinates = (
        int(index_left.x * width), int(index_left.y * height))

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)
    # TODO: tip of eye to eyebrow
    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)
    # angle_between_wrist_elbow_shoulder_right = get_angle_between_three_points(wrist_right_coordinates, elbow_right_coordinates, shoulder_right_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    distance_between_rightknee_leftknee = get_distance(
        knee_right_coordinates, knee_left_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)

    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    # condition for salute
    left_eyebrow = results.face_landmarks.landmark[359] if results.face_landmarks else None
    left_hand_middle_finger_tip = results.left_hand_landmarks.landmark[
        12] if results.left_hand_landmarks else None
    left_hand_middle_finger_mid = results.left_hand_landmarks.landmark[
        11] if results.left_hand_landmarks else None

    print('_'*45)
    if left_eyebrow is None:
        print(f'Left eyebrow is not visible - {left_eyebrow}')
    if left_hand_middle_finger_tip is None:
        print(
            f'Left hand middle finger tip is not visible - {left_hand_middle_finger_tip}')
    if left_hand_middle_finger_mid is None:
        print(
            f'Left hand middle finger mid is not visible - {left_hand_middle_finger_mid}')

    left_eyebrow_coordinates = (int(
        left_eyebrow.x * width), int(left_eyebrow.y * height)) if left_eyebrow else None
    left_hand_middle_finger_tip_coordinates = (int(left_hand_middle_finger_tip.x * width), int(
        left_hand_middle_finger_tip.y * height)) if left_hand_middle_finger_tip else None
    left_hand_middle_finger_mid_coordinates = (int(left_hand_middle_finger_mid.x * width), int(
        left_hand_middle_finger_mid.y * height)) if left_hand_middle_finger_mid else None

    # is_distance_between_left_tip_eyebrow_correct = get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates) <= 2 * get_distance(
    #     left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates) if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid else False

    if left_eyebrow and index_left:
        # print(
        #     f" dist {get_distance(left_eyebrow_coordinates,left_hand_middle_finger_tip_coordinates)}")
        # print(get_distance(
        #     left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates))

        # print(get_distance(left_eyebrow_coordinates,left_hand_middle_finger_tip_coordinates)/get_distance(
        #     left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates))
        print(get_distance(left_eyebrow_coordinates, index_left_coordinates))

    is_distance_between_left_tip_eyebrow_correct = True

    body_posture_check = body_posture > 170 and body_posture < 190
    back_posture_check = back_posture > 158 and back_posture < 210
    distance_between_rightshoulder_leftshoulder_check = distance_between_rightshoulder_leftshoulder < 47
    distance_between_rightknee_leftknee_check = distance_between_rightknee_leftknee < 25
    # print(distance_between_rightknee_leftknee)
    angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 280 and angle_between_wrist_elbow_shoulder_left < 340

    # print(angle_between_wrist_elbow_shoulder_left)

    if distance_left < 0 and distance_right < 0 and body_posture_check and back_posture_check and distance_between_rightshoulder_leftshoulder_check and \
            distance_between_rightknee_leftknee_check and angle_between_wrist_elbow_shoulder_left_check and is_distance_between_left_tip_eyebrow_correct:
        cv2.putText(frame, f'Correct Baye Salute',
                    (window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame
    else:
        cv2.putText(frame, f'Incorrect Baye Salute',
                    (window_size[0]-800, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not is_distance_between_left_tip_eyebrow_correct:
            cv2.putText(frame, f'Incorrect right hand salute', (
                window_size[0]-800, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not body_posture_check:
            cv2.putText(frame, f'Incorrect Body Posture', (
                window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not back_posture_check:
            cv2.putText(frame, f'Incorrect Back Posture', (
                window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not distance_between_rightshoulder_leftshoulder_check:
            cv2.putText(frame, f'Please face left side', (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not distance_between_rightknee_leftknee_check:
            cv2.putText(frame, f'Keep legs close together', (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not angle_between_wrist_elbow_shoulder_left_check:
            cv2.putText(frame, f'Incorrect salute', (
                window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def daine_Salute_old(results, frame):
    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    # check if body is visible
    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            hip_right.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ear_right.visibility < 0.7 or \
            knee_right.visibility < 0.7:
        cv2.putText(frame, "Face the right side", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)
    # TODO: tip of eye to eyebrow
    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    distance_between_rightknee_leftknee = get_distance(
        knee_right_coordinates, knee_left_coordinates)

    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    # condition for salute
    left_eyebrow = results.face_landmarks.landmark[359] if results.face_landmarks else None
    left_hand_middle_finger_tip = results.left_hand_landmarks.landmark[
        12] if results.left_hand_landmarks else None
    left_hand_middle_finger_mid = results.left_hand_landmarks.landmark[
        11] if results.left_hand_landmarks else None

    print('_'*45)
    if left_eyebrow is None:
        print(f'Left eyebrow is not visible - {left_eyebrow}')
    if left_hand_middle_finger_tip is None:
        print(
            f'Left hand middle finger tip is not visible - {left_hand_middle_finger_tip}')
    if left_hand_middle_finger_mid is None:
        print(
            f'Left hand middle finger mid is not visible - {left_hand_middle_finger_mid}')

    left_eyebrow_coordinates = (int(
        left_eyebrow.x * width), int(left_eyebrow.y * height)) if left_eyebrow else None
    left_hand_middle_finger_tip_coordinates = (int(left_hand_middle_finger_tip.x * width), int(
        left_hand_middle_finger_tip.y * height)) if left_hand_middle_finger_tip else None
    left_hand_middle_finger_mid_coordinates = (int(left_hand_middle_finger_mid.x * width), int(
        left_hand_middle_finger_mid.y * height)) if left_hand_middle_finger_mid else None

    is_distance_between_left_tip_eyebrow_correct = get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates) <= 2 * get_distance(
        left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates) if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid else False

    # if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid:

    #     print(get_distance(left_eyebrow_coordinates,
    #                        left_hand_middle_finger_tip_coordinates))
    #     print(get_distance(left_hand_middle_finger_tip_coordinates,
    #           left_hand_middle_finger_mid_coordinates))

    back_posture_check = back_posture > 158 and back_posture < 210
    body_posture_check = body_posture > 170 and body_posture < 196
    distance_between_rightshoulder_leftshoulder_check = distance_between_rightshoulder_leftshoulder < 55
    distance_between_rightknee_leftknee_check = distance_between_rightknee_leftknee < 25
    angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 250 and angle_between_wrist_elbow_shoulder_left < 310

    if distance_left > 0 and distance_right > 0 and back_posture_check and body_posture_check and distance_between_rightshoulder_leftshoulder_check and \
            distance_between_rightknee_leftknee_check and angle_between_wrist_elbow_shoulder_left_check and is_distance_between_left_tip_eyebrow_correct:
        cv2.putText(frame, f'Correct Daine Salute',
                    (window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame
    else:
        cv2.putText(frame, f'Incorrect Daine Salute',
                    (window_size[0]-800, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not is_distance_between_left_tip_eyebrow_correct:
            cv2.putText(frame, f'Incorrect right hand salute', (
                window_size[0]-800, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not back_posture_check:
            cv2.putText(frame, f'Incorrect back posture', (
                window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not body_posture_check:
            cv2.putText(frame, f'Incorrect body posture', (
                window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not distance_between_rightshoulder_leftshoulder_check:
            cv2.putText(frame, f'Please face right', (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not distance_between_rightknee_leftknee_check:
            cv2.putText(frame, f'Knees should be close to each other', (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if not angle_between_wrist_elbow_shoulder_left_check:
            cv2.putText(frame, f'do proper salute', (
                window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def front_salute_modified(results, frame):

    height, width, _ = frame.shape

    # ? angle between shoulder, elbow and wrist should be around 170 for both right hand
    # ? angle between center of ear, center of shoulder and center of hip should be around 180
    # ? distance betweeen wrist and hip should be less (need to find out the exact distance)
    # ? everything below the waist should ignored

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]

    # TODO: add visibility checks for all the landmarks so that user has to come closer
    if shoulder_right.visibility < 0.7 or shoulder_left.visibility < 0.7 or elbow_right.visibility < 0.7 \
            or elbow_left.visibility < 0.7 or wrist_right.visibility < 0.7 or wrist_left.visibility < 0.7 \
            or hip_right.visibility < 0.7 or hip_left.visibility < 0.7 \
            or ankle_right.visibility > 0.3 or ankle_left.visibility > 0.3:
        cv2.putText(frame, f'Please come closer. Only upper body should be visible',
                    (window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))

    shoulder_center_coordinates = (int((shoulder_right.x + shoulder_left.x)
                                   * width / 2), int((shoulder_right.y + shoulder_left.y) * height / 2))
    hip_center_coordinates = (int((hip_right.x + hip_left.x) * width / 2),
                              int((hip_right.y + hip_left.y) * height / 2))
    ear_center_coordinates = (int((ear_right.x + ear_left.x) * width / 2),
                              int((ear_right.y + ear_left.y) * height / 2))

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)

    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)
    angle_between_wrist_elbow_shoulder_right = get_angle_between_three_points(
        wrist_right_coordinates, elbow_right_coordinates, shoulder_right_coordinates)

    left_eyebrow = results.face_landmarks.landmark[359] if results.face_landmarks else None
    left_hand_middle_finger_tip = results.left_hand_landmarks.landmark[
        12] if results.left_hand_landmarks else None
    left_hand_middle_finger_mid = results.left_hand_landmarks.landmark[
        11] if results.left_hand_landmarks else None

    if left_eyebrow is None:
        cv2.putText(frame, f'left_eyebrow is None', (
            window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    if left_hand_middle_finger_tip is None:
        cv2.putText(frame, f'left_hand_middle_finger_tip is None', (
            window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    if left_hand_middle_finger_mid is None:
        cv2.putText(frame, f'left_hand_middle_finger_mid is None', (
            window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    if left_eyebrow is not None and left_hand_middle_finger_tip is not None and left_hand_middle_finger_mid is not None:
        left_eyebrow_coordinates = (
            int(left_eyebrow.x * width), int(left_eyebrow.y * height))
        left_hand_middle_finger_tip_coordinates = (int(
            left_hand_middle_finger_tip.x * width), int(left_hand_middle_finger_tip.y * height))
        left_hand_middle_finger_mid_coordinates = (int(
            left_hand_middle_finger_mid.x * width), int(left_hand_middle_finger_mid.y * height))

        is_distance_between_left_tip_eyebrow_correct = get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates) <= 1.75 * get_distance(
            left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates) if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid else False

        distance_between_rightwrist_righthip = get_distance(
            wrist_right_coordinates, hip_right_coordinates)

        # print(f'distance_between_rightwrist_righthip: {distance_between_rightwrist_righthip}')

        back_posture_check = back_posture > 160 and back_posture < 210
        distance_between_rightwrist_righthip_check = distance_between_rightwrist_righthip > 65 and distance_between_rightwrist_righthip < 90
        angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 308 and angle_between_wrist_elbow_shoulder_left < 323
        angle_between_wrist_elbow_shoulder_right_check = angle_between_wrist_elbow_shoulder_right > 165 and angle_between_wrist_elbow_shoulder_right < 195

        if back_posture_check and distance_between_rightwrist_righthip_check and angle_between_wrist_elbow_shoulder_left_check and is_distance_between_left_tip_eyebrow_correct and angle_between_wrist_elbow_shoulder_right_check:
            cv2.putText(frame, "Correct Front Salute Position",
                        (window_size[0]-600, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return True, frame

        else:
            cv2.putText(frame, "Incorrect Front Salute Position",
                        (window_size[0]-600, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if is_distance_between_left_tip_eyebrow_correct == False:
                cv2.putText(frame, "Incorrect Right Hand Position", (
                    window_size[0]-1000, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if back_posture_check == False:
                cv2.putText(frame, "Incorrect Back Posture", (
                    window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if distance_between_rightwrist_righthip_check == False:
                cv2.putText(frame, "Incorrect Distance Between Right Wrist and Right Hip", (
                    window_size[0]-1200, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if angle_between_wrist_elbow_shoulder_left_check == False:
                cv2.putText(frame, "Incorrect Angle Between Wrist, Elbow and Shoulder Left", (
                    window_size[0]-1200, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            return False, frame

    else:
        cv2.putText(frame, f'Face and Left hand not visible', (
            window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        return False, frame


def front_salute(results, frame):

    height, width, _ = frame.shape

    # angle between shoulder, elbow and wrist should be around 170 for both hands
    # angle between center of shoulder and center of hip and center of ankle should be around 180
    # angle between center of ear and center of shoulder and center of hip should be around 180
    # distance betweeen wrist and hip should be less (need to find out the exact distance)

    # TODO: add the face keypoints
    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]

    # check if body is visible
    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_right.visibility < 0.7 or hip_left.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ankle_left.visibility < 0.7 or ear_right.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7 or knee_right.visibility < 0.7:
        cv2.putText(frame, "Full body should be visible", (int(
            width/2), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    nose_coordinates = (int(nose.x * width), int(nose.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ankle_center_coordinates = midpoint(
        ankle_left_coordinates, ankle_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)

    angle_between_wrist_elbow_shoulder_right = get_angle_between_three_points(
        wrist_right_coordinates, elbow_right_coordinates, shoulder_right_coordinates)

    distance_between_knees = get_distance(
        knee_left_coordinates, knee_right_coordinates)
    distance_between_ankles = get_distance(
        ankle_left_coordinates, ankle_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)

    distance_nose_ear_right = check_direction(
        nose_coordinates, ear_right_coordinates)
    distance_nose_ear_left = check_direction(
        nose_coordinates, ear_left_coordinates)

    left_eyebrow = results.face_landmarks.landmark[359] if results.face_landmarks else None
    left_hand_middle_finger_tip = results.left_hand_landmarks.landmark[
        12] if results.left_hand_landmarks else None
    left_hand_middle_finger_mid = results.left_hand_landmarks.landmark[
        11] if results.left_hand_landmarks else None

    print('_'*45)
    if left_eyebrow is None:
        print(f'Left eyebrow is not visible - {left_eyebrow}')
    if left_hand_middle_finger_tip is None:
        print(
            f'Left hand middle finger tip is not visible - {left_hand_middle_finger_tip}')
    if left_hand_middle_finger_mid is None:
        print(
            f'Left hand middle finger mid is not visible - {left_hand_middle_finger_mid}')

    left_eyebrow_coordinates = (int(
        left_eyebrow.x * width), int(left_eyebrow.y * height)) if left_eyebrow else None
    left_hand_middle_finger_tip_coordinates = (int(left_hand_middle_finger_tip.x * width), int(
        left_hand_middle_finger_tip.y * height)) if left_hand_middle_finger_tip else None
    left_hand_middle_finger_mid_coordinates = (int(left_hand_middle_finger_mid.x * width), int(
        left_hand_middle_finger_mid.y * height)) if left_hand_middle_finger_mid else None

    is_distance_between_left_tip_eyebrow_correct = get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates) <= 1.75 * get_distance(
        left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates) if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid else False

    back_posture_check = back_posture > 160 and back_posture < 210
    body_posture_check = body_posture > 160 and body_posture < 200
    distance_between_knees_check = distance_between_knees > 25 and distance_between_knees < 80
    distance_between_ankles_check = distance_between_ankles > 5 and distance_between_ankles < 80
    distance_between_rightwrist_righthip_check = distance_between_rightwrist_righthip > 33 and distance_between_rightwrist_righthip < 55
    angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 308 and angle_between_wrist_elbow_shoulder_left < 323
    angle_between_wrist_elbow_shoulder_right_check = angle_between_wrist_elbow_shoulder_right > 170 and angle_between_wrist_elbow_shoulder_right < 210
    distance_ear_noses_check = distance_nose_ear_left < 0 and distance_nose_ear_right > 0

    if back_posture_check and body_posture_check and distance_between_knees_check and \
            distance_between_ankles_check and distance_between_rightwrist_righthip_check and \
            angle_between_wrist_elbow_shoulder_left_check and is_distance_between_left_tip_eyebrow_correct and angle_between_wrist_elbow_shoulder_right_check and \
            distance_ear_noses_check:
        cv2.putText(frame, "Correct Front Salute Position",
                    (window_size[0]-600, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        logger.info("Correct Front Salute Position")
        return True, frame
    else:
        cv2.putText(frame, "Incorrect Front Salute Position",
                    (window_size[0]-600, window_size[1]-500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        logger.info("Incorrect Front Salute Position")

        if is_distance_between_left_tip_eyebrow_correct == False:
            cv2.putText(frame, "Incorrect Right Hand Position", (
                window_size[0]-800, window_size[1]-450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect Right Hand Position")
            logger.info(f'get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates): {get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates)}: (160, 210)')
            logger.info(f'get_distance(left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates)): { get_distance(left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates)}: (160, 210)')

        if back_posture_check == False:
            cv2.putText(frame, "Incorrect Back Posture", (
                window_size[0]-800, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect back posture")
            logger.info(f'back_posture: {back_posture}: (160, 210)')
        if body_posture_check == False:
            cv2.putText(frame, "Incorrect Body Posture", (
                window_size[0]-800, window_size[1]-350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect body posture")
            logger.info(f'body_posture: {body_posture}: (160, 200)')
        if distance_between_knees_check == False:
            cv2.putText(frame, "Incorrect Distance Between Knees", (
                window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between knees')
            logger.info(f'distance_between_knees: {distance_between_knees}: (25, 80)')
        if distance_between_ankles_check == False:
            cv2.putText(frame, "Incorrect Distance Between Ankles", (
                window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between ankles')
            logger.info(f'distance_between_ankles: {distance_between_ankles}: (5, 80)')
        if distance_between_rightwrist_righthip_check == False:
            cv2.putText(frame, "Incorrect Distance Between left Wrist and left Hip", (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between rightwrist_righthip')
            logger.info(f'distance_between_rightwrist_righthip: {distance_between_rightwrist_righthip}: (33, 55)')
        if angle_between_wrist_elbow_shoulder_left_check == False:
            cv2.putText(frame, "Incorrect Angle Between right Wrist, Elbow and Shoulder", (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between right Wrist, Elbow and Shoulder')
            logger.info(f'angle_between_wrist_elbow_shoulder_left: {angle_between_wrist_elbow_shoulder_left}: (308, 323)')
        if angle_between_wrist_elbow_shoulder_right_check == False:
            cv2.putText(frame, "Keep Left hand straight", (
                window_size[0]-900, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between right Wrist, Elbow and Shoulder')
            logger.info(f'angle_between_wrist_elbow_shoulder_right: {angle_between_wrist_elbow_shoulder_right}: (170, 210)')
        if distance_ear_noses_check == False:
            cv2.putText(frame, "Keep head straight", (
                window_size[0]-900, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Keep head straight')
            logger.info(f'distance_ear_noses_check: {distance_ear_noses_check}: (distance_nose_ear_left < 0 and distance_nose_ear_right > 0)')
        return False, frame


def baye_salute_modified(results, frame):

    height, width, _ = frame.shape

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]

    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_right.visibility < 0.7 or hip_left.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ankle_left.visibility < 0.7 or ear_right.visibility < 0.7 or ear_left.visibility < 0.7 or \
            knee_left.visibility < 0.7 or knee_right.visibility < 0.7 or nose.visibility < 0.7:
        cv2.putText(frame, "Entire body not visible", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    nose_coordinates = (int(nose.x * width), int(nose.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ankle_center_coordinates = midpoint(
        ankle_left_coordinates, ankle_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)

    angle_between_wrist_elbow_shoulder_right = get_angle_between_three_points(
        wrist_right_coordinates, elbow_right_coordinates, shoulder_right_coordinates)

    distance_between_knees = get_distance(
        knee_left_coordinates, knee_right_coordinates)
    distance_between_ankles = get_distance(
        ankle_left_coordinates, ankle_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)

    distance_nose_ear_left = check_direction(
        nose_coordinates, ear_left_coordinates)
    print(distance_nose_ear_left)

    # written left but is actually right
    distance_nose_ear_right = check_direction(
        nose_coordinates, ear_right_coordinates)
    print(distance_nose_ear_right)

    back_posture_check = back_posture > 160 and back_posture < 210
    body_posture_check = body_posture > 160 and body_posture < 200
    distance_between_knees_check = distance_between_knees > 25 and distance_between_knees < 80
    distance_between_ankles_check = distance_between_ankles > 5 and distance_between_ankles < 80
    distance_between_rightwrist_righthip_check = distance_between_rightwrist_righthip > 33 and distance_between_rightwrist_righthip < 55
    distance_nose_ear_left_check = distance_nose_ear_right < 0

    angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 308 and angle_between_wrist_elbow_shoulder_left < 323
    angle_between_wrist_elbow_shoulder_right_check = angle_between_wrist_elbow_shoulder_right > 165 and angle_between_wrist_elbow_shoulder_right < 210

    left_eyebrow = results.face_landmarks.landmark[359] if results.face_landmarks else None
    left_hand_middle_finger_tip = results.left_hand_landmarks.landmark[
        12] if results.left_hand_landmarks else None
    left_hand_middle_finger_mid = results.left_hand_landmarks.landmark[
        11] if results.left_hand_landmarks else None

    if left_eyebrow is None:
        print(f'Left eyebrow is not visible - {left_eyebrow}')
    if left_hand_middle_finger_tip is None:
        print(
            f'Left hand middle finger tip is not visible - {left_hand_middle_finger_tip}')
    if left_hand_middle_finger_mid is None:
        print(
            f'Left hand middle finger mid is not visible - {left_hand_middle_finger_mid}')

    left_eyebrow_coordinates = (int(
        left_eyebrow.x * width), int(left_eyebrow.y * height)) if left_eyebrow else None
    left_hand_middle_finger_tip_coordinates = (int(left_hand_middle_finger_tip.x * width), int(
        left_hand_middle_finger_tip.y * height)) if left_hand_middle_finger_tip else None
    left_hand_middle_finger_mid_coordinates = (int(left_hand_middle_finger_mid.x * width), int(
        left_hand_middle_finger_mid.y * height)) if left_hand_middle_finger_mid else None

    is_distance_between_left_tip_eyebrow_correct = get_distance(left_eyebrow_coordinates, left_hand_middle_finger_tip_coordinates) <= 1.75 * get_distance(
        left_hand_middle_finger_tip_coordinates, left_hand_middle_finger_mid_coordinates) if left_eyebrow and left_hand_middle_finger_tip and left_hand_middle_finger_mid else False

    # ? for Baye salute check for distance_nose_left
    # ? for Daine salute check for distance_nose_right
    # print(f'distance_nose_ear_left: {distance_nose_ear_left}')

    if back_posture_check and body_posture_check and distance_between_knees_check and \
            distance_between_ankles_check and distance_between_rightwrist_righthip_check and \
            angle_between_wrist_elbow_shoulder_left_check and angle_between_wrist_elbow_shoulder_right_check and \
            distance_nose_ear_left_check:
        cv2.putText(frame, "Correct Baye Salute Position",
                    (window_size[0]-600, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        logger.info("Correct Baye Salute Position")
        return True, frame

    else:
        cv2.putText(frame, "Incorrect Baye Salute Position",
                    (window_size[0]-600, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        logger.info("Incorrect Baye Salute Position")

        if back_posture_check == False:
            cv2.putText(frame, "Incorrect Back Posture", (
                window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect back posture")
            logger.info(f'back_posture: {back_posture}: (160, 210)')
        if body_posture_check == False:
            cv2.putText(frame, "Incorrect Body Posture", (
                window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect body posture")
            logger.info(f'body_posture: {body_posture}: (160, 200)')
        if distance_between_knees_check == False:
            cv2.putText(frame, "Incorrect Distance Between Knees", (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between knees')
            logger.info(f'distance_between_knees: {distance_between_knees}: (25, 80)')
        if distance_between_ankles_check == False:
            cv2.putText(frame, "Incorrect Distance Between Ankles", (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between ankles')
            logger.info(f'distance_between_ankles: {distance_between_ankles}: (5, 80)')
        if distance_between_rightwrist_righthip_check == False:
            cv2.putText(frame, "Incorrect Distance Between left Wrist and left Hip", (
                window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between rightwrist_righthip')
            logger.info(f'distance_between_rightwrist_righthip: {distance_between_rightwrist_righthip}: (33, 55)')
        if angle_between_wrist_elbow_shoulder_left_check == False:
            cv2.putText(frame, "Incorrect Angle Between right Wrist, Elbow and Shoulder", (
                window_size[0]-800, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between right Wrist, Elbow and Shoulder')
            logger.info(f'angle_between_wrist_elbow_shoulder_left: {angle_between_wrist_elbow_shoulder_left}: (308, 323)')
        if angle_between_wrist_elbow_shoulder_right_check == False:
            cv2.putText(frame, "Keep Left hand straight", (
                window_size[0]-900, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between left Wrist, Elbow and Shoulder')
            logger.info(f'angle_between_wrist_elbow_shoulder_right: {angle_between_wrist_elbow_shoulder_right}: (165, 210)')
        if distance_nose_ear_left_check == False:
            cv2.putText(frame, "Face head to the left", (
                window_size[0]-900, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Face head to the left')
            logger.info(f'distance_nose_ear_left_check: {distance_nose_ear_left_check}: (< 0)')
        return False, frame


def daine_salute_modified(results, frame):

    height, width, _ = frame.shape

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]
    # or ear_left.visibility < 0.7
    if shoulder_right.visibility < 0.7 or elbow_right.visibility < 0.7 or wrist_right.visibility < 0.7 or \
            shoulder_left.visibility < 0.7 or elbow_left.visibility < 0.7 or wrist_left.visibility < 0.7 or \
            hip_right.visibility < 0.7 or hip_left.visibility < 0.7 or ankle_right.visibility < 0.7 or \
            ankle_left.visibility < 0.7 or ear_right.visibility < 0.7 or \
            knee_left.visibility < 0.7 or knee_right.visibility < 0.7:
        cv2.putText(frame, "Take a correct stance", (int(width/2),
                    int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return False, frame

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    nose_coordinates = (int(nose.x * width), int(nose.y * height))

    # get the center of the body
    shoulder_center_coordinates = midpoint(
        shoulder_left_coordinates, shoulder_right_coordinates)
    hip_center_coordinates = midpoint(
        hip_left_coordinates, hip_right_coordinates)
    ankle_center_coordinates = midpoint(
        ankle_left_coordinates, ankle_right_coordinates)
    ear_center_coordinates = midpoint(
        ear_left_coordinates, ear_right_coordinates)
    knee_center_coordinates = midpoint(
        knee_left_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    body_posture = get_angle_between_three_points(
        shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    angle_between_wrist_elbow_shoulder_left = get_angle_between_three_points(
        wrist_left_coordinates, elbow_left_coordinates, shoulder_left_coordinates)

    angle_between_wrist_elbow_shoulder_right = get_angle_between_three_points(
        wrist_right_coordinates, elbow_right_coordinates, shoulder_right_coordinates)

    distance_between_knees = get_distance(
        knee_left_coordinates, knee_right_coordinates)
    distance_between_ankles = get_distance(
        ankle_left_coordinates, ankle_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)
    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)

    # distance_nose_ear_right = check_direction(
    #     nose_coordinates, ear_right_coordinates)
    # print(distance_nose_ear_right)

    distance_nose_ear_left = check_direction(
        nose_coordinates, ear_left_coordinates)
    # print(distance_nose_ear_left)

    back_posture_check = back_posture > 160 and back_posture < 210
    body_posture_check = body_posture > 160 and body_posture < 200
    distance_between_knees_check = distance_between_knees > 25 and distance_between_knees < 80
    distance_between_ankles_check = distance_between_ankles > 5 and distance_between_ankles < 80
    distance_between_rightwrist_righthip_check = distance_between_rightwrist_righthip > 33 and distance_between_rightwrist_righthip < 55
    angle_between_wrist_elbow_shoulder_left_check = angle_between_wrist_elbow_shoulder_left > 308 and angle_between_wrist_elbow_shoulder_left < 323
    angle_between_wrist_elbow_shoulder_right_check = angle_between_wrist_elbow_shoulder_right > 170 and angle_between_wrist_elbow_shoulder_right < 210
    distance_nose_ear_right_check = distance_nose_ear_left > 0

    if back_posture_check and body_posture_check and distance_between_knees_check and \
            distance_between_ankles_check and distance_between_rightwrist_righthip_check and angle_between_wrist_elbow_shoulder_left_check and angle_between_wrist_elbow_shoulder_right_check \
            and distance_nose_ear_right_check:
        cv2.putText(frame, "Correct Daine Salute Position",
                    (window_size[0]-600, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        logger.info("Correct Daine Salute Position")
        return True, frame
    else:
        cv2.putText(frame, "Incorrect Daine Salute Position",
                    (window_size[0]-600, window_size[1]-400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        logger.info("Incorrect Daine Salute Position")
        if back_posture_check == False:
            cv2.putText(frame, "Incorrect Back Posture", (
                window_size[0]-800, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect back posture")
            logger.info(f'back_posture: {back_posture}: (160, 210)')
        if body_posture_check == False:
            cv2.putText(frame, "Incorrect Body Posture", (
                window_size[0]-800, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info("Incorrect body posture")
            logger.info(f'body_posture: {body_posture}: (160, 200)')
        if distance_between_knees_check == False:
            cv2.putText(frame, "Incorrect Distance Between Knees", (
                window_size[0]-800, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between knees')
            logger.info(f'distance_between_knees: {distance_between_knees}: (25, 80)')
        if distance_between_ankles_check == False:
            cv2.putText(frame, "Incorrect Distance Between Ankles", (
                window_size[0]-800, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between ankles')
            logger.info(f'distance_between_ankles: {distance_between_ankles}: (5, 80)')
        if distance_between_rightwrist_righthip_check == False:
            cv2.putText(frame, "Incorrect Distance Between left Wrist and left Hip", (
                window_size[0]-800, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect distance between rightwrist_righthip')
            logger.info(f'distance_between_rightwrist_righthip: {distance_between_rightwrist_righthip}: (33 55)')
        if angle_between_wrist_elbow_shoulder_left_check == False:
            cv2.putText(frame, "Incorrect Angle Between right Wrist, Elbow and Shoulder", (
                window_size[0]-800, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between right Wrist, Elbow and Shoulder')
            logger.info(f'angle_between_wrist_elbow_shoulder_left: {angle_between_wrist_elbow_shoulder_left}: (308, 323)')
        if angle_between_wrist_elbow_shoulder_right_check == False:
            cv2.putText(frame, "Keep Left hand straight", (
                window_size[0]-900, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Incorrect Angle Between left Wrist, Elbow and Shoulder')
            logger.info(f'ngle_between_wrist_elbow_shoulder_right: {angle_between_wrist_elbow_shoulder_right}: (170, 210)')
        if distance_nose_ear_right_check == False:
            cv2.putText(frame, "Face head to the right", (
                window_size[0]-900, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            logger.info(f'Face head to the right')
            logger.info(f'distance_nose_ear_right_check: {distance_nose_ear_right_check}: (> 0)')
        return False, frame


def Daine_transition_pos1(results, frame):
    # to check leg distance and left facing
    # distance between left leg feet and floor should be minimal (we will use angle approach around 0-10)
    # distance between right leg feet and floor should be there (we will use angle approach around 35-55 with the horizontal drawn on ground)

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    angle_between_knees_and_hip = get_angle_between_three_points(
        knee_left_coordinates, hip_center_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    # body_posture = get_angle_between_three_points(shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    # distance_between_rightknee_leftknee = get_distance(knee_right_coordinates, knee_left_coordinates)

    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)
    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    # right side facing
    # body_posture > 170 and body_posture < 190 and \
    if distance_left > 0 and distance_right > 0 and \
            back_posture > 158 and back_posture < 195 and \
            distance_between_rightshoulder_leftshoulder < 16 and \
            distance_between_rightwrist_righthip < 25 and \
            distance_between_leftwrist_lefthip < 45 and \
            angle_between_knees_and_hip < 35:
        cv2.putText(frame, f'Correct Right transition',
                    (window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame
    else:
        cv2.putText(frame, f'Incorrect Right Transition',
                    (window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Back posture: {back_posture}', (
            window_size[0]-500, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between shoulders: {distance_between_rightshoulder_leftshoulder}', (
            window_size[0]-500, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right wrist and right hip: {distance_between_rightwrist_righthip}', (
            window_size[0]-500, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between left wrist and left hip: {distance_between_leftwrist_lefthip}', (
            window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Angle between knees and hip: {angle_between_knees_and_hip}', (
            window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def Baye_transition_pos1(results, frame):
    # to check leg distance and left facing
    # distance between left leg feet and floor should be minimal (we will use angle approach around 0-10)
    # distance between right leg feet and floor should be there (we will use angle approach around 35-55 with the horizontal drawn on ground)

    shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
    wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
    wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
    hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
    ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
    ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
    ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
    knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
    left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
    right_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
    left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
    right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

    height, width, _ = frame.shape

    shoulder_right_coordinates = (
        int(shoulder_right.x * width), int(shoulder_right.y * height))
    elbow_right_coordinates = (
        int(elbow_right.x * width), int(elbow_right.y * height))
    wrist_right_coordinates = (
        int(wrist_right.x * width), int(wrist_right.y * height))
    shoulder_left_coordinates = (
        int(shoulder_left.x * width), int(shoulder_left.y * height))
    elbow_left_coordinates = (
        int(elbow_left.x * width), int(elbow_left.y * height))
    wrist_left_coordinates = (
        int(wrist_left.x * width), int(wrist_left.y * height))
    hip_right_coordinates = (int(hip_right.x * width),
                             int(hip_right.y * height))
    hip_left_coordinates = (int(hip_left.x * width), int(hip_left.y * height))
    ankle_right_coordinates = (
        int(ankle_right.x * width), int(ankle_right.y * height))
    ankle_left_coordinates = (
        int(ankle_left.x * width), int(ankle_left.y * height))
    ear_right_coordinates = (int(ear_right.x * width),
                             int(ear_right.y * height))
    ear_left_coordinates = (int(ear_left.x * width), int(ear_left.y * height))
    knee_left_coordinates = (int(knee_left.x * width),
                             int(knee_left.y * height))
    knee_right_coordinates = (
        int(knee_right.x * width), int(knee_right.y * height))
    left_toe_coordinates = (int(left_toe_from_pose.x * width),
                            int(left_toe_from_pose.y * height))
    right_toe_coordinates = (
        int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
    left_heel_coordinates = (
        int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
    right_heel_coordinates = (
        int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
    ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
        (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
    shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
        (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
    hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
        (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
    knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
        (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

    angle_between_knees_and_hip = get_angle_between_three_points(
        knee_left_coordinates, hip_center_coordinates, knee_right_coordinates)

    back_posture = get_angle_between_three_points(
        ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
    # body_posture = get_angle_between_three_points(shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

    distance_between_rightshoulder_leftshoulder = get_distance(
        shoulder_right_coordinates, shoulder_left_coordinates)
    # distance_between_rightknee_leftknee = get_distance(knee_right_coordinates, knee_left_coordinates)

    distance_between_rightwrist_righthip = get_distance(
        wrist_right_coordinates, hip_right_coordinates)
    distance_between_leftwrist_lefthip = get_distance(
        wrist_left_coordinates, hip_left_coordinates)
    distance_left = check_direction(
        left_toe_coordinates, left_heel_coordinates)
    distance_right = check_direction(
        right_toe_coordinates, right_heel_coordinates)

    # left side facing
    # body_posture > 170 and body_posture < 190 and \
    if distance_left < 0 and distance_right < 0 and \
            back_posture > 158 and back_posture < 210 and \
            distance_between_rightshoulder_leftshoulder < 30 and \
            distance_between_rightwrist_righthip < 35 and \
            distance_between_leftwrist_lefthip < 45 and \
            angle_between_knees_and_hip < 35:
        cv2.putText(frame, f'Correct Left transition',
                    (window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return True, frame
    else:
        cv2.putText(frame, f'Incorrect Left Transition',
                    (window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Back Posture: {back_posture}', (
            window_size[0]-500, window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between shoulders: {distance_between_rightshoulder_leftshoulder}', (
            window_size[0]-500, window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between right wrist and right hip: {distance_between_rightwrist_righthip}', (
            window_size[0]-500, window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Distance between left wrist and left hip: {distance_between_leftwrist_lefthip}', (
            window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Angle between knees and hip: {angle_between_knees_and_hip}', (
            window_size[0]-500, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return False, frame


def Piche_position(results, frame):
    # check if face landmarks and face is visible
    if results.face_landmarks is None:
        # logic here
        shoulder_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
        elbow_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
        wrist_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
        shoulder_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
        elbow_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
        wrist_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
        hip_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
        hip_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
        ankle_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
        ankle_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
        ear_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
        ear_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR]
        knee_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
        knee_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
        left_toe_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
        right_toe_from_pose = results.pose_landmarks.landmark[
            mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
        left_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HEEL]
        right_heel_from_pose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HEEL]

        height, width, _ = frame.shape

        shoulder_right_coordinates = (
            int(shoulder_right.x * width), int(shoulder_right.y * height))
        elbow_right_coordinates = (
            int(elbow_right.x * width), int(elbow_right.y * height))
        wrist_right_coordinates = (
            int(wrist_right.x * width), int(wrist_right.y * height))
        shoulder_left_coordinates = (
            int(shoulder_left.x * width), int(shoulder_left.y * height))
        elbow_left_coordinates = (
            int(elbow_left.x * width), int(elbow_left.y * height))
        wrist_left_coordinates = (
            int(wrist_left.x * width), int(wrist_left.y * height))
        hip_right_coordinates = (
            int(hip_right.x * width), int(hip_right.y * height))
        hip_left_coordinates = (int(hip_left.x * width),
                                int(hip_left.y * height))
        ankle_right_coordinates = (
            int(ankle_right.x * width), int(ankle_right.y * height))
        ankle_left_coordinates = (
            int(ankle_left.x * width), int(ankle_left.y * height))
        ear_right_coordinates = (
            int(ear_right.x * width), int(ear_right.y * height))
        ear_left_coordinates = (int(ear_left.x * width),
                                int(ear_left.y * height))
        knee_left_coordinates = (
            int(knee_left.x * width), int(knee_left.y * height))
        knee_right_coordinates = (
            int(knee_right.x * width), int(knee_right.y * height))
        left_toe_coordinates = (
            int(left_toe_from_pose.x * width), int(left_toe_from_pose.y * height))
        right_toe_coordinates = (
            int(right_toe_from_pose.x * width), int(right_toe_from_pose.y * height))
        left_heel_coordinates = (
            int(left_heel_from_pose.x * width), int(left_heel_from_pose.y * height))
        right_heel_coordinates = (
            int(right_heel_from_pose.x * width), int(right_heel_from_pose.y * height))
        ear_center_coordinates = (int((ear_left_coordinates[0] + ear_right_coordinates[0])/2), int(
            (ear_left_coordinates[1] + ear_right_coordinates[1])/2))
        shoulder_center_coordinates = (int((shoulder_left_coordinates[0] + shoulder_right_coordinates[0])/2), int(
            (shoulder_left_coordinates[1] + shoulder_right_coordinates[1])/2))
        hip_center_coordinates = (int((hip_left_coordinates[0] + hip_right_coordinates[0])/2), int(
            (hip_left_coordinates[1] + hip_right_coordinates[1])/2))
        knee_center_coordinates = (int((knee_left_coordinates[0] + knee_right_coordinates[0])/2), int(
            (knee_left_coordinates[1] + knee_right_coordinates[1])/2))

        angle_between_knees_and_hip = get_angle_between_three_points(
            knee_left_coordinates, hip_center_coordinates, knee_right_coordinates)

        back_posture = get_angle_between_three_points(
            ear_center_coordinates, shoulder_center_coordinates, hip_center_coordinates)
        # body_posture = get_angle_between_three_points(shoulder_center_coordinates, hip_center_coordinates, knee_center_coordinates)

        distance_between_rightshoulder_leftshoulder = get_distance(
            shoulder_right_coordinates, shoulder_left_coordinates)
        distance_between_rightknee_leftknee = get_distance(
            knee_right_coordinates, knee_left_coordinates)

        distance_between_rightwrist_righthip = get_distance(
            wrist_right_coordinates, hip_right_coordinates)
        distance_between_leftwrist_lefthip = get_distance(
            wrist_left_coordinates, hip_left_coordinates)

        if back_posture > 174 and back_posture < 186 and \
                distance_between_rightshoulder_leftshoulder > 124 and distance_between_rightshoulder_leftshoulder < 146 and \
                distance_between_rightwrist_righthip > 39 and distance_between_rightwrist_righthip < 65 and \
                distance_between_leftwrist_lefthip > 24 and distance_between_leftwrist_lefthip < 51 and \
                angle_between_knees_and_hip > 334 and angle_between_knees_and_hip < 346:
            # angle between angle_between_knees_and_hip is the differenciating factor between back savdhan and back trainsition
            #distance_between_rightknee_leftknee > 0 and distance_between_rightknee_leftknee < 10000
            cv2.putText(frame, f'Correct Piche transition', (
                window_size[0]-500, window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return True, frame
        else:
            cv2.putText(frame, f'Incorrect Piche Transition', (
                window_size[0]-500, window_size[1]-300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Back posture: {back_posture}', (window_size[0]-500,window_size[1]-250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Distance between right shoulder and left shoulder: {distance_between_rightshoulder_leftshoulder}', (window_size[0]-500,window_size[1]-200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Distance between right wrist and right hip: {distance_between_rightwrist_righthip}', (window_size[0]-500,window_size[1]-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Distance between left wrist and left hip: {distance_between_leftwrist_lefthip}', (window_size[0]-500,window_size[1]-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Angle between knees and hip: {angle_between_knees_and_hip}', (window_size[0]-500,window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            return False, frame
    else:
        return False, frame


def Mud_fnc(var1, var2, var3, mud_array=[0, 0, 0]):
    flag = False
    if var1:
        mud_array[0] = 1
    if var2 and mud_array[0]:
        mud_array[1] = 1
    if var3 and mud_array[0] and mud_array[1]:
        mud_array[2] = 1
    if sum(mud_array) == 3:
        flag = True
    return flag, mud_array


def Khade_Khade_Daine_Mud(results, frame, mud_array):
    var1, frame = savdhan(results, frame)
    if var1:
        print("Front check done")
    var2, frame = Daine_transition_pos1(results, frame)
    if var2:
        print("Daine transition done")
    var3, frame = right_side_savdhan(results, frame)
    if var3:
        print("Right side check done")
        print("Complete Daine Mud done")
    flag, mud_array = Mud_fnc(var1, var2, var3, mud_array)
    if flag:
        cv2.putText(frame, f'Khade Khade Daine Mud',
                    (window_size[0]-550, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return flag, frame, mud_array


def Khade_Khade_Baye_Mud(results, frame, mud_array):

    var1, frame = savdhan(results, frame)
    if var1:
        print("Front check done")
    var2, frame = Baye_transition_pos1(results, frame)
    if var2:
        print("Baye transition done")
    var3, frame = left_side_savdhan(results, frame)
    if var3:
        print("Left side check done")
        print("Complete Baye Mud done")
    flag, mud_array = Mud_fnc(var1, var2, var3, mud_array)
    if flag:
        cv2.putText(frame, f'Khade Khade Baye Mud',
                    (window_size[0]-550, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return flag, frame, mud_array


def Khade_Khade_Peeche_Mud(results, frame, mud_array):
    var1, frame = savdhan(results, frame)
    if var1:
        print("Front check done")
    var2, frame = Piche_position(results, frame)
    if var2:
        print("Piche position done")
    var3, frame = savdhan_back(results, frame)
    if var3:
        print("Back check done")
        print("Complete Peeche Mud done")
    flag, mud_array = Mud_fnc(var1, var2, var3, mud_array)
    if flag:
        cv2.putText(frame, f'Khade Khade Peeche Mud complete',
                    (window_size[0]-550, window_size[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return flag, frame, mud_array


# TODOs
# Salute logic
# use the distance substraction logic for front, daine and baye salute
# front has one -ve one +ve
# daine has two +ve
# baye has two -ve
