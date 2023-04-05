import cv2
import util

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
        results, frame = util.run_mediapipe_holistic(frame)

        if results.pose_landmarks:
            if choice == 1:
                activity_check_flag, frame = util.savdhan(
                    results, frame)
            elif choice == 2:
                activity_check_flag, frame = util.vishram(results, frame)
            elif choice == 3:
                activity_check_flag, frame = util.baye_salute_modified(
                    results, frame)
            elif choice == 4:
                activity_check_flag, frame = util.daine_salute_modified(
                    results, frame)
            elif choice == 5:
                activity_check_flag, frame = util.front_salute(
                    results, frame)

        util.draw_styled_landmarks(frame, results)
        frame = cv2.resize(frame, (720, 850))
        cv2.imshow("Frame", frame)

        # writer.write(frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            # writer.release()
            break

    cap.release()
    cv2.destroyAllWindows()
    # writer.release()


main(path)
