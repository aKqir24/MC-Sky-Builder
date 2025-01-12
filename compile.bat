@echo off
set name=MC-Sky-Builder
set icon=resource\icon.ico
set module_path=libraries
set work_folder=exe

if Python --version if Python -m PyInstaller --version (
    Python -m PyInstaller -w -i %icon% -D --optimize 2 --clean  --workpath %work_folder% --contents-directory %module_path% -n %name% window.py
) else (
    echo "Please update `python` then install PyInstaller and read the error logs!!"
)
