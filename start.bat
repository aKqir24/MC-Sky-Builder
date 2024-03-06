color f0
@echo off
cls

echo You Might Need Some Internet To Install The Requirements
@echo off
cls
pip install keyboard
cls
pip install colorama
cls
pip install pillow
cls
pip install numpy
cls

if  errorlevel 1 goto ERROR
echo Requirements Installed
cls
echo Running Program...
cls
echo Running Program..
cls
echo Running Program.
cls
echo Running Program..
cls
echo Running Program...
cls
goto EOF 


:ERROR

echo Please Install Python Or Check Your Internet Connection
cmd /k
exit /b 1
:EOF 

python mcsky.py