#!/bin/bash

   #------------------------------------------------------------------------------#
   # For Linux Enviroments, You Need To Run This In Wine Inside The Source Folder # 
   #------------------------------------------------------------------------------#

# Errors & Fixes Sources Strings!!
Wine_Error="Error: Wine is not Installed!!"
Python_Error="Error: Python is not Installed in Wine!!"
Wine_Fix="You Can Refer To This Ducumentation For Assistance:"
Wine_Fix_Web="https://www.winehq.org/pipermail/wine-devel/2002-January/003468.html"
Pip_Check="Checking Dependencies [It will install them with PIP if not found]"
Pip_Error="Please Connect To The Internet To Install The Dependencies"

depend=("wine" "python" "numpy" "pillow" "opencv-python")

# Checks If Wine & Python Is Installed 
function check_depend {	
  for package in {0..1}; do
    if ${depend[$package]} --version ; then
       clear ; echo "Checking ${depend[$package]}..." ; sleep 2
       clear ; echo "'${depend[$package]}' is Installed!!" ; sleep 2
    else
       if ["$package" == "2"]; then
          clear ; echo $Python_Error
       else
          clear ; echo $Wine_Error ; echo $Wine_Fix ; echo $Wine_Fix_Web
       fi
    fi
  done
}

# Checks & Installs The Python Dependencies
function check_py_depend {
  clear ; echo $Pip_Check ; sleep 1
  for package in {2..4}; do
    clear ; echo "Checking '${depend[$package]}'..." ; sleep 2
    if wine pip install ${depend[$package]} ; then
       clear ; echo "'${depend[$package]}' is Installed" ; sleep 2 ; clear
    else
       clear ; echo $Pip_Error
    fi
  done
}

# Runnning The Program In Wine & Handles Errors!!
function program { 
  if wine python $(pwd)/window.py; then
    clear ; echo "Program Exited!!"
    if pkill wine-run; then
       continue
    else
       pkill sh
    fi
  else
    clear ; echo "Program Exited Due Too.."
    echo "Error: Your Running The Program Inside The Wine Directory"
    echo "Fix: Please Consider Running It In The Os Directory" 
    echo "    (cd source folder then sh wine-run.sh)"
  fi 
}

function progress {
while :; do
  progress_text=("." ".." "..." " ")
  for loading in {0..2}; do 
     clear ; echo "Running Program${progress_text[$loading]}" ; sleep 1
  done
done
}

# Options to Choose When running the Program
case ${1,,} in
	--ignore-depend)
                program "Program Is Running!!"
        ;;
	--help)
		clear
		echo " MC-Sky-Builder:"
		echo "      // by default (the program first takes time to verify the dependencies)"
		echo "      --ignore-depend (to skip this process)"
	;;
	*)
		check_depend ; check_py_depend ; program & progress
esac
