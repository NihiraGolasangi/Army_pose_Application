@REM start a flask server
CALL env/Scripts/activate.bat
@REM for the below command to woek you need a python virtual environmen
set FLASK_APP=pose_backend.py
set FLASK_ENV=development
start flask run
@REM the below command will start a flask server on port 5000 on system default browser
@REM start http://127.0.0.1:5000/

:loop
ping 127.0.0.1 -n 2 >nul
IF %ERRORLEVEL% NEQ 0 (
   echo Server not started yet, waiting for 10 seconds
   timeout /t 10
   goto loop
) ELSE (
   echo Server started
@REM    start chrome http://localhost:8000
    start http://127.0.0.1:5000/
)