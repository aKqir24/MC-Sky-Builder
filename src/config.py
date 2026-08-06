"""
  Distributes the default ''Elements'' used, in the modules
"""

# Program Information
__author__: "Akqir"
__version__: "1.2.0"
__program_name__: "MC-Sky-Builder"
__description__: "Converts an Image into a sky-overlay pack for minecraft..."

from json import dump, load
from tempfile import gettempdir
from time import sleep, strftime
from PIL import Image, ImageFont, ImageTk
from os import getenv, path, remove as rm, mkdir, makedirs, name, rename
from customtkinter.windows.widgets.font import FontManager

#? Image Input / Output Values
image_details: list = [] # [1] = imgpath, [2] = img-filename
ext, curve_radius = [".png", 2]

# interface values
rel = 'flat'
yp, x, y , yb = [ 225, 15, 3, 2 ]
supported_resolutions = {0: 256, 1: 512, 2: 1024, 3: 2048}
db, b, b2, f, ab = [ "#283149","#404b69", "#333e5f", "#dbedf3", "#00818a" ]

# folder and file paths
noto_font = str(path.join('resource', 'noto_sans.ttf'))
try:
    noto_font_name = ImageFont.truetype(noto_font, 9).getname()[1]
except Exception:
    noto_font_name = "sans-serif"

font_details = [
    (noto_font_name, 8, 'normal'),
    (noto_font_name, 10, 'normal'),
    (noto_font_name, 10, 'bold'),
    (noto_font_name, 12, 'normal'),
    (noto_font_name, 12, 'bold')
]
title_icon_path = str(path.join('resource', 'title', ''))
home_user= path.expanduser("~")
tempdir = f'{gettempdir()}/MC-Sky-Builder'
FontManager.linux_font_path = tempdir

from pathlib import Path

#? Identify the 'OS' your using...
default_output_path = str(Path.home() / "Desktop")
if not path.exists(default_output_path):
    default_output_path = str(Path.home())

if name == "nt":
  config_folder = getenv('APPDATA')+'\\mcskymaker' if getenv('APPDATA') else str(Path.home() / 'AppData' / 'Roaming' / 'mcskymaker')
  config_file = config_folder + "\\settings.json"
  try:
    from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
    desktop_regkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    with OpenKey(HKEY_CURRENT_USER, desktop_regkey) as key:
      default_output_path = path.expandvars( QueryValueEx(key, "Desktop")[0] )
  except Exception:
    pass

else:
    config_folder = str(Path.home() / '.mcskymaker')
    config_file = config_folder + "/settings.json"

# config dictionary / default config
configs = { "Image_Size": 256, "Output_Folder": default_output_path,
            "Convert_To_Mcpack": False, "Convert_To_Zip": False}

#? Current config's
def readconfig():
  with open(config_file, 'r') as raw_config:
    json_open = load(raw_config)
    for key in configs:
        configs[f"{key}"] = json_open[f'{key}']

def writeconfig():
    with open(config_file, 'w') as raw_config:
        dump(configs, raw_config, indent=4)
