#!/bin/bash
#For Linux Enviroment You Need To Run It In Wine
Error="Please install 'Wine' then install 'python' in wine."
if dpkg -l | grep ^ii | grep -i wine ; then
  clear
  wine python window.py
else
  echo $Error
fi
