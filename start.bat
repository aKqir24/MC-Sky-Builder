color f0
@echo off
cls
echo You Might Need Some Internet To Install The Requirements


pip install keyboard
cls
echo Installing Requirements.
pip install colorama
cls
echo Installing Requirements..
pip install pillow
cls
echo Installing Requirements...
pip install numpy
cls


if  errorlevel 1 goto ERROR

goto EOF 

:ERROR

echo Please Install Python Or Check Your Internet Connection
pause
cmd /k
exit /b 1
:EOF
 
cls
echo Running Program.
cls
echo Running Program..
cls
echo Running Program...
cls
echo Running Program....

python mcsky.py

if  errorlevel 1 goto ERROR

goto EOF 
echo Requirements Installed!!

:ERROR

echo Please Install Python
cmd /k
exit /b 1

:EOF
echo Running Program...