""" 
    Worker works around with Files, and Directory

 - setting the cofiguration file, ui, and directory
 - creating or preparing the temporary files needed
 - managing the filenames, extension and other details
 - zipping the complete output of create
 
"""

import winreg
from all_val import *
from json import dump, load
from shutil import copytree, copy, rmtree
from uuid import uuid4 as generate_random_uuid
from os import path, remove as rm, mkdir, rename
from tkinter import filedialog, Toplevel, Label, StringVar, messagebox, _tkinter
from PIL import Image, ImageTk

class GetImageDetails:
  def __init__(self, imgpath):
    self.imgpath = imgpath
    
  def getimagename(self):
    imgext = GetImageDetails.getimgext(self)
    rmpackex = self.imgpath.replace(imgext, "")
    # Remove The dirname to get the filename
    default_index = 1
    getimgpath = rmpackex
    imgpathfori = getimgpath+" "
    while getimgpath[:-default_index].startswith('/') == False:
      cl= default_index+1
      default_index = cl
      rmdirtxt = (imgpathfori[:-default_index])
      if rmdirtxt.endswith('/') == True:
        thefilename = imgpathfori.replace(rmdirtxt, "")
        imagefilename = (thefilename[:-1])
        image_details.append(imagefilename)
        break
  
  def getimgext(self):
    image_details.append(self.imgpath)
    imgext = Image.open(self.imgpath).format
    theimgext = "."+imgext.lower()
    image_details.append(theimgext)
    return theimgext

class ToDoDuringStartup:
  config_folder = config_dir.replace("\\settings.json", "")

  def makethetempdir(self):
    if path.exists(tempdir): pass
    else: mkdir(tempdir)
    if path.exists(tempdir+'sky_output'): pass
    else: mkdir(tempdir+'sky_output')
    if path.exists(self.config_folder): pass
    else: mkdir(self.config_folder)
    return self
          
  # Set The Default Output Folder Path
  def setdefaults(self):
    if path.exists(config_dir):pass
    else:
      chosen_res = "256"
      with winreg.OpenKey(winreg.HKEY_CURRENT_USER, dsktp_regkey) as key:
        userdesktop = path.expandvars( winreg.QueryValueEx(key, "Desktop")[0] ).replace("\\", "/")
        with open(config_dir, 'w') as writeconfig:
          configuration = { "Image_Size": chosen_res, "Convert_To_Zip": False, 
                "Convert_To_Mcpack": False, "Outputfolder_Path": userdesktop }
          readusingjson = dump(configuration, writeconfig, indent=4)
    return self

class ConfigManagement:
  config_dict = {"image_res": 256, "ch_convert": True}
  
  # Get the config value then update to a dict{}
  ImgResConfigValue = lambda self, imgresvalue : self.config_dict.update({'image_res': imgresvalue})
  CnvrtToMcpackValue = lambda self, chmcpackval: self.config_dict.update({'ch_convert': chmcpackval})
  OutPathConfigValue = lambda self, outpathvalue: self.config_dict.update({'output_path': outpathvalue})
  CustomImgResConfigValue = lambda self, imgresvalue: self.config_dict.update({'image_custom_res': imgresvalue})
    
  def writesettingsconfig(self):
    readconfig = open(config_dir, 'r')
    readusingjson = load(readconfig)
    config_dict = self.config_dict
    try:
      if config_dict['output_path'] == "":
        userpath = readusingjson['Outputfolder_Path']
      else: userpath = config_dict['output_path']
    except KeyError: userpath = readusingjson['Outputfolder_Path']
    if config_dict.get('image_custom_res') == None:
      try: chosen_res = config_dict['image_res']
      except KeyError: chosen_res = readusingjson['Image_Size']
    else: chosen_res = config_dict['image_custom_res']

    getchconmcpack = config_dict.get('ch_convert"')
    if getchconjavzip == None: getchconjavzip = readusingjson['Convert_Pack']

    with open(config_dir, 'w') as writeconfig:
      configuration = { "Image_Size": chosen_res, "Convert_To_Zip": getchconjavzip,
                        "Convert_To_Mcpack": getchconmcpack, "Outputfolder_Path": userpath }
      readusingjson = dump(configuration, writeconfig, indent=4)
      config_dict.clear()
  
class SettingsMultiOptions:
    def __init__(self, imgresolution, packzipval, packmcpackval ):
      self.packzipval = packzipval
      self.imgresolution = imgresolution
      self.packmcpackval = packmcpackval
     
    def outputres(self):
      chosen_res = self.imgresolution.get()
      if chosen_res == int(0): chosen_res = 256
      elif chosen_res == int(10): chosen_res = 512
      elif chosen_res == int(20): chosen_res = 1024
      elif chosen_res == int(30): chosen_res = 2048
      ConfigManagement().ImgResConfigValue(chosen_res)
        
    def checkzipconvert(self):
      thepackzipvalue = self.packzipval.get()
      if thepackzipvalue == False: thepackzipvalue = False
      elif thepackzipvalue == True: thepackzipvalue = True
      ConfigManagement().CnvrtToJavZipValue(thepackzipvalue)
      
    def checkmcpackconvert(self):
      thepackmcpackchvalue = self.packmcpackval.get()
      if thepackmcpackchvalue == False: thepackmcpackchvalue = False
      elif thepackmcpackchvalue == True: thepackmcpackchvalue = True
      ConfigManagement().CnvrtToMcpackValue(thepackmcpackchvalue)
    
class MkJsonPackDetailsFile:
  pack_des = "This SkyOverlay Was Made By The Help Of §cAkqir's (§bMC §fSky Builder) Software..." 
  def makethemanifest():
    uuid1 = generate_random_uuid()
    uuid2 = generate_random_uuid()
    pack_name = GetImageDetails.getimagename()
    # For Bedrock Write The Manifest File 
    with open(tempdir+'manifest.json', 'w') as writejson:
      manifestfile =  { "format_version": 1, "header": { 
                        "description": MkJsonPackDetailsFile.pack_des,
                        "name": image_details[2]+" (Sky Overlay)", "uuid": str(uuid1), 
                        "version": [1, 0, 0], "min_engine_version": [1, 12, 0]}, "modules": [ { 
                        "description": "", "type": "resources", "uuid": str(uuid2), "version": [1, 0, 0] } ] }
      dump(manifestfile, writejson, sort_keys=True, skipkeys=1, indent=3)
    
    def makethepackmeta():
      with open('pack.json', 'w') as writepckmeta:
        pack_des = FileManagement.pack_des.replace("§c", "").replace("§b", "").replace("§f", "")
        packmeta = { "pack": { "pack_format": 1, "description": pack_des } }
        dump(packmeta, writepckmeta, sort_keys=True, skipkeys=1, indent=3)
      os.rename('pack.json', 'pack.mcmeta')

    def packfolrenamer():
      pass

class ZipMcpackOrBoth:
  def PackToZip():
    pass
  def PackToMcpack():
    pass