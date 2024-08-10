#!/bin/bash
"
For Linux Enviroment You Need To Run It In Wine
"
if dpkg -l | grep ^ii | grep -i wine ; then
  wine python window.py
