#!/bin/bash

#For Linux Enviroment You Need To Run This In Wine
Wine_Error="Error: Please install 'Wine' then install 'python' in wine."
Wine_Fix="You Can Refer To This Ducumentation For Assistance: https://www.winehq.org/pipermail/wine-devel/2002-January/003468.html"
Pip_Error="Please Connect To The Internet To Install The Dependencies"

echo "Checking Wine..."
if wine --version ; then
  echo "Wine Installed!!"
  echo "Checking Dependencies [It will install them with PIP if not found]"
  
  if wine pip install numpy; then
    if wine pip install pillow; then
      echo "Program Launched!!"
      
      if wine python window.py ; then
      echo "Program Exited!!"
      else
        echo "Error: You forgot to install 'python' in wine!! "
        echo $Wine_Fix
      fi
    else
    echo $Pip_Error
    fi
  else
    echo $Pip_Error
  fi
else
  echo $Wine_Error
  echo $Wine_Fix
fi
