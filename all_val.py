"""

  Distributes the ''Elements'' used, in the modules

""" 

from json import dump, load
from time import sleep, strftime
from PIL import Image, ImageFont, ImageTk
from os import getenv, path, remove as rm, mkdir, makedirs, name, rename

# [1] = imgpath, [2] = img-filename
image_details: list = []

# default relief
rel = 'flat'

# color scheme
db, b, b2, f, ab = [ "#283149","#404b69", "#333e5f", "#dbedf3", "#00818a" ]
# place coords
yp, x, y , yb = [ 225, 15, 3, 2 ]

# output configuration 
ext, curve_radius = [".png", 2]

# font verification
font_details = [(ImageFont.truetype(resource_folder('res\\noto_sans.ttf'), 9).getname()[1], 8), ('Segoe UI',10,'normal')] 

#? Identify the 'OS' your using!!
if name == "nt":
  tempdir = getenv('TEMP')+'\\MC-Sky-Builder\\'
  config_dir = getenv('APPDATA')+'\\mcskymaker\\settings.json' 
  config_folder = config_dir.replace("\\settings.json", "")
  def default_output_path():
    desktop_regkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, desktop_regkey) as key:
      userdesktop = path.expandvars( winreg.QueryValueEx(key, "Desktop")[0] )
    return userdesktop
    
elif name == "posix":
  tempdir = '~/.cache'
  config_dir = '~/.config/mcskymaker/settings.json'
  config_folder = config_dir.replace("/settings.json", "")
  def default_output_path():
    userdesktop = '~'
    return userdesktop

else: print("Operating System not supported!!")

#? Current config's
def readconfig():
  with open(config_dir, 'r') as readconfig:
    readusingjson = load(readconfig)
    img_res = readusingjson['Image_Size']
    out_path = readusingjson['Outputfolder_Path']
    zip_pack_ch = readusingjson['Convert_To_Zip']
    mc_pack_ch = readusingjson['Convert_To_Mcpack']
  return [img_res, out_path, zip_pack_ch, mc_pack_ch]

def writeconfig(chosen_res, getchconjavzip, getchconmcpack, userpath):
  with open(config_dir, 'w') as writeconfig:
    configuration = { "Image_Size": chosen_res, "Convert_To_Zip": getchconjavzip,
                      "Convert_To_Mcpack": getchconmcpack, "Outputfolder_Path": userpath }
    readusingjson = dump(configuration, writeconfig, indent=4)

#* default configuration
config_dict = {"image_res": 256, "mc_convert": False, "jv_convert": False}