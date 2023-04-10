from ultralytics import YOLO
import cv2
import util
import numpy as np

#Load the model
model = YOLO('yolov8n.pt')

path = '/Users/atharvaparikh/Desktop/atCode/Project/DIAT/End2End Implemenations/Army_pose_Application/raw videos/Atharva Savdhan near.mp4'

def main(path):
    cap = cv2.VideoCapture(path)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    choice = int(input("Enter your Choice: "))

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    util.window_size = (frame_width, frame_height)

    # writer = cv2.VideoWriter(f'ProcessedVideo01.avi', cv2.VideoWriter_fourcc(
    #     *'MJPG'), 10, (frame_width, frame_height))

    count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        count += 1
        if count%10 != 0:
            continue
        frame = cv2.flip(frame, 1)
        frame = cv2.blur(frame, (3, 3))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            # writer.release()
            break

        results = model(frame)
        #results will be a list of detections - one detection with multiple bboxes

        boxes = results[0].boxes
        person_count = [int(box.cls) for box in boxes if int(box.cls) == 0].count(0)
        if person_count == 0:
            cv2.putText(frame, "No Person Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Please Stand in Front of the Camera", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            continue
        elif person_count > 1:
            cv2.putText(frame, "Multiple Persons Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "One person at a time is allowed", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            continue
        else:
            #proper one person
            bbox = np.asarray(boxes[0].xyxy[0])
            xmin, ymin, xmax, ymax = bbox
            #convert all the values to int
            xmin = int(xmin)
            ymin = int(ymin)
            xmax = int(xmax)
            ymax = int(ymax)
            # subframe = frame[ymin:ymax, xmin:xmax]

            # Increase the image size after cropping
            #================================================================================================ 
            height = frame.shape[0]
            width = frame.shape[1]
            adjuster = 100 #? change this value upon experimentation
            
            #increase the size of the image
            #increase the height
            if ymin - adjuster < 0: ymin = 0 
            else: ymin = ymin - adjuster

            if ymax + adjuster > height: ymax = height
            else: ymax = ymax + adjuster

            #increase the width
            if xmin - adjuster < 0: xmin = 0
            else: xmin = xmin - adjuster

            if xmax + adjuster > width: xmax = width
            else: xmax = xmax + adjuster

            subframe = frame[ymin:ymax, xmin:xmax]
            resize_to = (250, 500)
            subframe = cv2.resize(subframe, resize_to)
            results, frame = util.run_mediapipe_holistic(subframe)
            #================================================================================================
            
            #Blank frame logic
            ##================================================================================================ 
            # #put this frame in a fixed size frame
            # #create a blank frame
            # resize_to = (250, 500)
            # subframe = cv2.resize(subframe, resize_to) #TODO: this frame size needs to be fixed and properly chosen
            # # blank_image = np.zeros(util.window_size, np.uint8)
            # #create a 3d blank image
            # x = 0
            # y = 0
            # width = subframe.shape[1]
            # height = subframe.shape[0]
            # # blank_image = np.zeros((util.window_size[0], util.window_size[1], 3), np.uint8)
            
            # blank_image = np.zeros((height + 200, width + 200, 3),np.uint8)
            # print(f'Blank Image Shape: {blank_image.shape}')
            # print(f'Subframe Shape: {subframe.shape}')
            # blank_image[100:height+100, 100:width+100] = subframe
            # cv2.imshow("Imposed person", blank_image)

            # results, frame = util.run_mediapipe_holistic(frame)
            ##================================================================================================

            #! exception pending here
            if results.pose_landmarks:
                if choice == 1:
                    activity_check_flag, frame = util.savdhan(results, frame)
                elif choice == 2:
                    activity_check_flag, frame = util.vishram(results, frame)
                elif choice == 3:
                    activity_check_flag, frame = util.baye_salute_modified(results, frame)
                elif choice == 4:
                    activity_check_flag, frame = util.daine_salute_modified(results, frame)
                elif choice == 5:
                    activity_check_flag, frame = util.front_salute(results, frame)

            util.draw_styled_landmarks(frame, results)
            # frame = cv2.resize(frame, (720, 850))
        
        cv2.imshow("Plotted Frame", frame)
        # writer.write(frame)

    cap.release()
    cv2.destroyAllWindows()
    # writer.release()

main(path)

#TODOs
# 1. The feedback has to be provided on the main frame while the check is being done on the subframe
# 2. Mainframe video will be rendered 
# 3. Use angle logic instead of distance based logic

# A. Savdhan:
#    - angle between both legs X degrees
#    - angle of armpits 
#    - body posture
#    - back posture

# B. Vishram
#    - angle between both legs
#    - wrist visibility should be less than 0.3
#    - back posture
#    - body posture

# C. Front Salute
#    - All savdhan checks
#    - angle of the right hand elbow

# 4. Show the feedback on the frontend
# 5. 