#!/bin/bash

#For Linux Enviroment You Need To Run It In Wine
Wine_Error="Please install 'Wine' then install 'python' in wine."
if dpkg -l | grep ^ii | grep -i wine ; then
  wine --verion
  if wine python window.py ; then
    echo "Program Launched!!"
  else
    echo "You forgot to install 'python' in wine!! " 
  fi
else
  echo $Wine_Error
fi
