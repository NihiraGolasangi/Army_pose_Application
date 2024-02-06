
# HUMAN POSE ESTIMATION - DESIGNED FOR ARMY DRILL EXERCISES

https://github.com/NihiraGolasangi/Army_pose_Application/assets/74126218/89067f20-2d46-4068-af84-4969369c4bd5



The traditional method of army training, which relies on a single coordinator to constantly supervise the training, presents several challenges. One such challenge is the requirement for constant supervision. To address these limitations, this paper proposes a new method that automates the inspection process during training of essential activities such as Salute, Vishram, and Savdhan.

### Technologies Used

- Python
- Mediapipe
- OpenCV
- YOLOV-8

<img src="Reference for Keypoints/Hand Points.png" width="300" height="200" position="centre">
<img src="Reference for Keypoints/Pose Points.png" width="500" height="200" position="centre">

##### SALUTE

In the Indian Army, a salute is executed by an open palm gesture with the fingers, thumb together, and the middle finger almost touching the hatband or forehead, making an angle of around 45 degrees at the elbow. Legs are stretched straight, knees should be touched, with an angle (30 degrees) between ankles.

##### SAVDHAN

Savdhan (attention) is performed by standing up straight with heels together, making an angle of 30 degrees, and having straight arms at the sides, closer to the hip. The chin should be at level, and the eyes should look straight ahead.

##### VISHRAM
Vishram (Stand at ease) is performed by relaxing knees, with a considerable distance between legs and interlocking fingers behind the back. Wrists and elbows of both hands should not be visible. The chin should be level, and the eyes should look straight ahead.


Through the utilization of pose estimation algorithms and techniques, the system accurately tracks and interprets human body movements. The system's offline functionality allows users to perform activities and record videos without requiring a continuous internet connection, providing convenience and flexibility.

### Dataset
- Recorded videos of seven individuals with varying heights, performing a set of activities, and these activities were recorded under different lighting conditions.
- Furthermore, to introduce variability in the dataset, each person performed the activities at different distances from the screen.
- By incorporating these factors, such as height, lighting condition, and distance from the screen, the dataset offers a comprehensive and diverse range of scenarios for analysis and evaluation. Depending on the type of drill activity, the videos in the dataset have a time frame between 5 and 10s.



### Process:

- After evaluating various pose detection models like Mediapipe, OpenPose, and AlphaPose, Mediapipe was chosen for its superior keypoints plotting and stability.
- The system focuses on army drill exercises, adhering to strict predefined rules for body postures, hand and leg positions, etc.
- The process involves extracting key points such as shoulders, elbows, wrists, ears, hips, ankles, knees, and nose using Mediapipe's models. - Visibility criteria were set to >0.7 to ensure all body parts are visible. Once visibility conditions are met, the model checks angles and distances between body parts against predefined military standards. Any deviations trigger an error display on the user screen.
- For angle estimation between keypoints, a formula utilizing the math.atan2 function is used:

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)) 

   Where, (x1, y1), (x2, y2), and (x3, y3) represent the coordinates of three key points in a 2D space. We utilize the math.atan2(y, x) function, which computes the angle (in radians) between the positive x-axis and the point (x, y).

- To measure the distance between keypoints, another formula is used:

    s_sq_difference += (p_i - q_i) ** 2
   distance = s_sq_difference ** 0.5 

   Where, p and q, represent the coordinates of distinct body landmarks or joints in a 2D space. The term "s_sq_difference" accumulates the sum of squared differences for each coordinate, denoted as p_i and q_i for the i-th coordinate (x or y) of keypoints p and q, respectively.

### YOLOV-8

- The testing revealed challenges in distance variations between body parameters, influenced by proximity to the screen and camera specifications.
- Multiple users or varying camera setups affected accuracy. To address this, the YOLOv8 model was adopted for its speed and precision. This model efficiently detects individuals and automatically generates cropped frames with 100px padding on each side.
- This preprocessing step is crucial, as it provides sufficient context for the subsequent use of the Mediapipe model. The padding around the person enhances Mediapipe's ability to accurately identify and track individuals in the image.
- The cropped frames are then resized to a predefined size of 250 * 500 px, ensuring stable and consistent representation of individuals across varying distances in the image.
- When the cropped frame is resized, the range of distances in the image becomes more stable. This is because individuals standing farther from the screen will appear almost the same size as those standing closer to the screen due to resizing.
- As a result, the range of distances in the image becomes more consistent.

