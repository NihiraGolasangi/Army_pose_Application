REM start a flask server
CALL env/Scripts/activate.bat
REM for the below command to woek you need a python virtual environmen
set FLASK_APP=pose_backend.py
set FLASK_ENV=development
flask run
REM the below command will start a flask server on port 5000 on system default browser
start http://127.0.0.1:5000/