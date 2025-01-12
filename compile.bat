set name=MC-Sky-Builder
set icon=resource\icon.ico
set module_path=libraries
set work_folder=exe

rem Compile To Exe
Python -m PyInstaller -w -i %icon% -D --optimize 2 --clean  --workpath %work_folder% --contents-directory %module_path% -n %name% window.py
