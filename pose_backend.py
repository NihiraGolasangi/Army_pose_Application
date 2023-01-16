from flask import Flask, render_template, Response, request
import sqlite3
import cv2
import datetime
import time
import os
import sys
import numpy as np
from threading import Thread
import util


global capture, rec_frame, grey, neg, face, rec, out, today
switch = 0
rec = 0
start_angle = 0
choice = 0
today = datetime.datetime.now().strftime("%Y_%m_%d-%I_%H_%M_%S")
activity_check_flag = False


try:
    # Check if video directory exists, if not create it.
    dirname = "Performance Videos"
    if not (os.path.isdir(dirname)):
        os.mkdir(dirname)
except OSError as error:
    print(error)


# instatiate flask app
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1100)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1100)

# camera = None

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
util.window_size = (frame_width, frame_height)
# util.window_size = (800, 600)

# iwriter = cv2.VideoWriter(f'Performance Videos/ProcessedVideo_{today}.mp4',cv2.VideoWriter_fourcc(*'MP4V'),10, (frame_width, frame_height)) #writes for default starting 5 sec
# swriter = cv2.VideoWriter(f'Performance Videos/ProcessedVideo_salute_{today}.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 10, (frame_width, frame_height)) #writer for when correct salute is detected

# TODO: start variable needs to be defined as global to be used in the function
# TODO: writers need to be global, started and stopped in between as execution proceeds


def record(out):
    global rec_frame
    while (rec):
        time.sleep(0.05)
        out.write(rec_frame)


def gen_frames_pose(a=1):  # generate frame by frame from camera

    mud_array = []
    start = time.time()
    chk = False
    start_angle = 0
    # global iwriter, swriter
    # iwriter = cv2.VideoWriter(f'Performance Videos/ProcessedVideo_{today}.mp4', cv2.VideoWriter_fourcc(
    #     *'MP4V'), 10, (frame_width, frame_height))  # writes for default starting 5 sec
    # swriter = cv2.VideoWriter(f'Performance Videos/ProcessedVideo_salute_{today}.mp4', cv2.VideoWriter_fourcc(
    #     *'MP4V'), 10, (frame_width, frame_height))  # writer for when correct salute is detected

    while True:
        ok, frame = camera.read()
        # flipping to make it more intuitive for the user
        frame = cv2.flip(frame, 1)
        end = time.time()
        if not ok:
            print('Video Over or not accessible')
            # frame = np.zeros((512, 512, 1), dtype="uint8")
            # TODO: add a blank screen with error message using numpy
        else:
            frame = cv2.blur(frame, (3, 3))
            # TODO: frame skipping logic to be added here
            results, frame = util.run_mediapipe_holistic(frame)
            choice = a
            # choice = request.args.get('choice')
            global correct
            correct = 0

            # Perform activity according to user input
            global activity_check_flag
            if results.pose_landmarks:
                if choice == 1:
                    activity_check_flag, frame = util.savdhan_front(
                        results, frame)
                elif choice == 2:
                    activity_check_flag, frame = util.vishram(results, frame)
                elif choice == 3:
                    activity_check_flag, frame = util.baye_salute(
                        results, frame)
                elif choice == 4:
                    activity_check_flag, frame = util.Daine_Salute(
                        results, frame)
                elif choice == 5:
                    activity_check_flag, frame = util.front_salute(
                        results, frame)
                elif choice == 6:
                    if not chk:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Daine_Mud(
                            results, frame, [0, 0, 0])
                        chk = True
                    else:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Daine_Mud(
                            results, frame, mud_array)
                elif choice == 7:
                    if not chk:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Baye_Mud(
                            results, frame, [0, 0, 0])
                        chk = True
                    else:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Baye_Mud(
                            results, frame, mud_array)
                elif choice == 8:
                    if not chk:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Peeche_Mud(
                            results, frame, [0, 0, 0])
                        chk = True
                    else:
                        activity_check_flag, frame, mud_array = util.Khade_Khade_Peeche_Mud(
                            results, frame, mud_array)
                else:
                    print('Wrong choice')

            else:
                cv2.putText(frame, "Please ensure full body is visible to the camera",
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            util.draw_styled_landmarks(frame, results)

            # ================================= WRITE VIDEOS ==============================================

            # if end-start <= 20 and not correct:
            #     iwriter.write(frame)

            # if activity_check_flag and not correct:
            #     correct = 1
            #     last_flag = True
            #     if start_angle == 0:
            #         start_angle = time()

            # if last_flag and start_angle != 0:
            #     if time() - start_angle <= 20:
            #         swriter.write(frame)

        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass


@app.route('/')
def index():
    return render_template('register.html')


@ app.route('/index', methods=['POST'])
def info():
    global i, n, activity
    i = request.form.get("id", False)
    n = request.form.get("name", False)
    activity = int(request.form.get("activity_name", False))
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames_pose(activity), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/thankyou')
def thankyou():
    try:
        if correct == 1:
            os.remove(f'Performance Videos/ProcessedVideo_{today}.mp4')
            filename = f'ProcessedVideo_salute_{today}.mp4'
        elif correct == 0:
            os.remove(f'Performance Videos/ProcessedVideo_salute_{today}.mp4')
            filename = f'ProcessedVideo_{today}.mp4'
    except:
        print('Videos not found')
        pass

    # iwriter.release()
    # swriter.release()

    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    query = 'INSERT INTO test  VALUES (?, ?, ?, ?,?)'
    fname = f'{os.getcwd()}\Performance Videos\ProcessedVideo_{today}'
    print(f"{i}, {n}, {activity},{activity_check_flag},{fname}")
    # C:\Users\Lenovo\Desktop\WORK\DIAT Repo\Send\Performance Videos\ProcessedVideo_2022_12_20-10_22_09_46
    # C:\Users\Lenovo\Desktop\WORK\DIAT Repo\Send\Performance Videos\ProcessedVideo_2022_12_20-10_22_26_56
    params = (i, n, activity, fname, activity_check_flag)
    conn.execute(query, params)

    conn.commit()
    print("Records created successfully")
    conn.close()

    return render_template("thankyou.html")


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera, choice
    if request.method == 'POST':

        if request.form.get('click') == 'Capture':
            global capture
            capture = 1

        elif request.form.get('stop') == 'Stop/Start':

            if (switch == 1):
                switch = 0
                camera.release()
                # cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        # elif request.form.get('rec') == 'Start/Stop Recording':
        #     global rec, out
        #     rec = not rec
        #     if (rec):
        #         now = datetime.datetime.now()
        #         fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #         out = cv2.VideoWriter('vid_{}.avi'.format(
        #             str(now).replace(":", '')), fourcc, 20.0, (640, 480))
        #         # Start new thread for recording the video
        #         thread = Thread(target=record, args=[out,])
        #         thread.start()
        #     elif (rec == False):
        #         out.release()

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
