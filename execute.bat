REM start a flask server
set FLASK_APP=pose_backend.py
set FLASK_ENV=development
flask run
REM the below command will start a flask server on port 5000 on system default browser
start http://127.0.0.1:5000/