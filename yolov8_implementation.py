from ultralytics import YOLO
import cv2
import util
import numpy as np

#Load the model
model = YOLO('yolov8n.pt')

path = '/Users/atharvaparikh/Desktop/atCode/Project/DIAT/End2End Implemenations/Army_pose_Application/Testing Videos/Salute_/video_20220719_093025.mp4'

def main(path):
    cap = cv2.VideoCapture(path)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    choice = int(input("Enter your Choice: "))

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    util.window_size = (850, 900)

    # writer = cv2.VideoWriter(f'ProcessedVideo01.avi', cv2.VideoWriter_fourcc(
    #     *'MJPG'), 10, (frame_width, frame_height))

    while (cap.isOpened()):
        ret, frame = cap.read()
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
            continue
        elif person_count > 1:
            cv2.putText(frame, "Multiple Persons Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            continue
        else:
            #proper one person
            bbox = np.asarray(boxes[0].xyxy[0])
            xmin, ymin, xmax, ymax = bbox
            frame2 = frame[int(ymin):int(ymax), int(xmin):int(xmax)]
            #TODO: take some additional area from the frame if possible
            #TODO: We need to fix a size for the frame2 and resize the frame2 to that size

        results, frame = util.run_mediapipe_holistic(frame2)
        # results, frame = util.run_mediapipe_holistic(frame)

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
        cv2.imshow("Frame", frame)
        cv2.imshow("Frame2", frame2)

        # writer.write(frame)

    cap.release()
    cv2.destroyAllWindows()
    # writer.release()

main(path)