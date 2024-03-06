color f0
@echo off
cls
echo You Might Need Some Internet To Install The Requirements

echo Installing Requirements 0/4
cls
echo Installing Requirements 1/4
pip install keyboard
cls
echo Installing Requirements 2/4
pip install colorama
cls
echo Installing Requirements 3/4
pip install pillow
cls
echo Installing Requirements 4/4
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
rem God Is Good All The Time :)
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