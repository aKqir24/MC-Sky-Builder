#!/bin/bash

##########################################################################
# For Linux Enviroment You Need To Run This In Wine In The Source Folder # 
##########################################################################

# Errors & Fixes Sources Strings!!
Wine_Error="Error: Wine not installed!!"
Python_Error="Error: Python Is Not Installed In Wine!!"
Wine_Fix="You Can Refer To This Ducumentation For Assistance:"
Wine_Fix_Web="https://www.winehq.org/pipermail/wine-devel/2002-January/003468.html"
Pip_Check="Checking Dependencies [It will install them with PIP if not found]"
Pip_Error="Please Connect To The Internet To Install The Dependencies"

# Checks If Wine & Python Is Installed 
export WINEDBUG=-all
clear ; echo "Checking Wine..." ; sleep 2
if wine --version ; then
  clear ; echo "Wine is Installed!!" ; sleep 2
  clear ; echo "Checking Python..." ; sleep 2
  if wine python --version ; then
    clear ; echo "Python is Installed!!" ; sleep 1

    # Checks & Installs The Python Dependencies
    sleep 2 ; clear ; echo $Pip_Check ; sleep 2
    clear ; echo "Checking 'numpy'..." ; sleep 2
    if wine pip install numpy; then
	clear ; echo "'numpy' is Intalled" ; sleep 2
	clear ; echo "Checking 'pillow'..." ; sleep 2
      if wine pip install pillow; then 
	clear ; echo "'pillow' is Installed"; sleep 2

	# Runnning The Program In Wine!!
	clear ; echo "Running The Program!!" ; sleep 2
        if wine python $(pwd)/window.py; then
          echo "Program Exited!!"
        else
	  clear ; echo "Program Exited Due Too.."
          echo "Error: Your Running The Program Inside The Wine Directory"
	  echo "Fix: Please Consider Running It In The Os Directory" 
	  echo "    (cd source folder then sh wine python window.py)"
        fi
      else
        clear ; echo $Pip_Error
      fi
    else
      clear ; echo $Pip_Error
    fi
  else
    clear ; echo $Python_Error
  fi
else
 clear ; echo $Wine_Error ; echo $Wine_Fix ; echo $Wine_Fix_Web
fi
