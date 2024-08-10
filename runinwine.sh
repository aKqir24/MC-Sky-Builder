#!/bin/bash

#For Linux Enviroment You Need To Run This In Wine
Wine_Error="Error: Please install 'Wine' then install 'python' in wine."
Wine_Fix="You Can Refer To This Ducumentation For Assistance: https://www.winehq.org/pipermail/wine-devel/2002-January/003468.html"
if dpkg -l | grep ^ii | grep -i wine ; then
  echo "Checking Wine..."
  wine --version
  if wine pip --version; then
    echo "Install Dependencies..."
    wine pip install numpy
    wine pip install pillow
    echo "Program Launched!!"
    if wine python window.py ; then
      echo "Program Exited!!"
    else
      echo "Error: You forgot to install 'python' in wine!! "
      echo $Wine_Fix
    fi
  else
    echo "Please Connect To The Internet To Install The Dependencies"
  fi
else
  echo $Wine_Error
  echo $Wine_Fix
fi
