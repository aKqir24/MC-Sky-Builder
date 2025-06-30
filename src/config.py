"""
  Distributes the ''Elements'' used, in the modules
""" 
from tempfile import gettempdir
from tkinter import PhotoImage
from json import dump, load
from time import sleep, strftime
from PIL import Image, ImageFont, ImageTk
from os import getenv, path, remove as rm, mkdir, makedirs, name, rename

#? Image Input / Output Values
image_details: list = [] # [1] = imgpath, [2] = img-filename
ext, curve_radius = [".png", 2]

# interface values
rel = 'flat'
yp, x, y , yb = [ 225, 15, 3, 2 ]
db, b, b2, f, ab = [ "#283149","#404b69", "#333e5f", "#dbedf3", "#00818a" ]

# folder and file paths
noto_font = str(path.join('resource', 'noto_sans.ttf'))
font_details = [(ImageFont.truetype(noto_font, 9).getname()[1], 8), ('Segoe UI',10,'normal')]
title_icon_path = path.join('resource', 'title', '')
home_user= path.expanduser("~")
tempdir = f'{gettempdir()}/MC-Sky-Builder'

#? Identify the 'OS' your using...
if name == "nt":
  config_folder = getenv('APPDATA')+'\\mcskymaker' 
  config_file = config_folder+"\\settings.json"
  from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx 
  desktop_regkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER, desktop_regkey) as key:
    default_output_path = path.expandvars( winreg.QueryValueEx(key, "Desktop")[0] )
    
elif name == "posix": 
    config_folder = f'{home_user}/.config/mcskymaker'
    config_file = config_folder+"/settings.json"
    default_output_path = home_user

# config dictionary / default config
configs = { "Image_Size": 256, "Output_Folder": default_output_path, 
            "Convert_To_Mcpack": False, "Convert_To_Zip": False}

#? Current config's
def readconfig():
  with open(config_file, 'r') as raw_config:
    json_open = load(raw_config) 
    for key in configs: 
        configs[f"{key}"] = json_open[f'{key}'] 

def writeconfig(chosen_res, getchconjavzip, getchconmcpack, userpath):
  with open(config_file, 'w') as raw_config:
    config_inputs = [ chosen_res, userpath, getchconmcpack, getchconjavzip, userpath ]
    for key in configs:
        for input in config_inputs:
            if not input == "": configs[f"{key}"] = input

    readusingjson = dump(configs, raw_config, indent=4)
