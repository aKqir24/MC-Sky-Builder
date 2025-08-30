""" 
    Worker works around with Files, and Directory

 - setting the configuration file, ui, and directory
 - creating or preparing the temporary files needed
 - managing the filenames, extension and other details
 - zipping the complete output of create
 
"""

from config import * 
from shutil import copytree, copy, move, rmtree, make_archive
from tkinter import filedialog, Toplevel, Label, StringVar, messagebox, _tkinter

class GetImageDetails:
  def __init__(self, imgpath):
    self.imgpath = imgpath

  #? Get the filename of an image 
  def getimagename(self):
    imgext = GetImageDetails.getimgext(self)
    rmpackex = self.imgpath.replace('jpg', 'jpeg').replace(imgext, "")

    # Remove The dirname to get the filename
    default_index, getimgpath = ( 1, rmpackex )
    imgpathfori = getimgpath+" "
    while getimgpath[:-default_index].startswith('/') == False:
      cl = default_index+1
      default_index = cl
      rmdirtxt = (imgpathfori[:-default_index])
      if rmdirtxt.endswith('/') == True:
        thefilename = imgpathfori.replace(rmdirtxt, "")
        imagefilename = (thefilename[:-1])
        image_details.append(imagefilename)
        break
  
  #? Get the file image extension/format
  def getimgext(self):
    image_details.append(self.imgpath)
    imgext = Image.open(self.imgpath).format
    theimgext = "."+imgext.lower()
    image_details.append(theimgext)
    print("Image Path: "+image_details[0])
    print("Image Format: "+theimgext)
    return theimgext

class ToDoDuringStartup:
  #? Make a temporary working folder
  def makethetempdir(self):
    if not path.exists(tempdir): mkdir(tempdir)
    if not path.exists(config_folder): mkdir(config_folder)
    return self
          
  #? Set the default output folder path
  def setdefaults(self):
    # chosen_res, getchconjavzip, getchconmcpack, userpath
    if not path.exists(config_file): writeconfig()
    readconfig()
    return self
      
class ConfigManagement:
  #* Simply send the values of your options in the config
    def __init__(self, output_resolution, pack_zip_val, pack_mcpack_val):
      self.output_resolution = output_resolution
      self.pack_zip_val=pack_zip_val
      self.pack_mcpack_val=pack_mcpack_val
      self.stored_config = configs
      self.custom_recent_resolution=None
      self.scale_recent_resolution=None

    userpath = lambda self, folder: self.stored_config.update({"Output_Folder": folder})

    def outputres(self, resolution):
      scale_resolution=self.output_resolution.get()
      if resolution > 4 and resolution is not None:
        self.custom_recent_resolution=resolution
        chosen_resolution = self.custom_recent_resolution
      elif supported_resolutions[resolution] in supported_resolutions \
              and not self.scale_recent_resolution == supported_resolutions[resolution]:
        chosen_resolution=supported_resolutions[resolution]
        print(supported_resolutions[resolution])
        self.custom_recent_resolution=None
      else:
          if self.custom_recent_resolution != None:
            chosen_resolution=self.custom_recent_resolution
          else:
            chosen_resolution=supported_resolutions[resolution]
          print(3)

      self.scale_recent_resolution=supported_resolutions[scale_resolution]
      self.stored_config.update({"Image_Size": chosen_resolution})

    def write_settings_config(self):
        self.outputres(self.output_resolution.get()) 
        self.stored_config.update({"Convert_To_Zip": self.pack_zip_val.get()})
        self.stored_config.update({"Convert_To_Mcpack": self.pack_mcpack_val.get()})
        writeconfig()
    
class MkJsonPackDetailsFile:
  pack_des = "This SkyOverlay Was Made By Using §cAkqir's §f(§bMC §fSky Builder) Software..." 
  def makethemanifest(self):
    from uuid import uuid4 as generate_random_uuid 

    #? For Bedrock Write The Manifest File 
    with open(tempdir+image_details[2]+".mcpack"+"\\"+'manifest.json', 'w') as writejson:
      manifestfile =  { "format_version": 1, "header": { 
                        "description": self.pack_des,
                        "name": image_details[2]+" (Sky Overlay)", "uuid": str(generate_random_uuid()), 
                        "version": [1, 0, 0], "min_engine_version": [1, 12, 0]}, "modules": [ { 
                        "description": "", "type": "resources", "uuid": str(generate_random_uuid()),
                        "version": [1, 0, 0] } ] }
      dump(manifestfile, writejson, sort_keys=True, skipkeys=1, indent=3)
    return self

  def makethepackmeta(self):
    #? For Java Write The Meta File 
    with open(tempdir+image_details[2]+".zip"+"\\"+'pack.mcmeta', 'w') as writepckmeta:
      pack_des = MkJsonPackDetailsFile.pack_des.replace("§c", "").replace("§b", "").replace("§f", "")
      packmeta = { "pack": { "pack_format": 1, "description": self.pack_des } }
      dump(packmeta, writepckmeta, sort_keys=True, skipkeys=1, indent=3)
    return self 

  # TODO: Enhance the pack_icon maker  
  def makepackicon (self, image_right, pack_folder, pack_icon_name):
    copy(tempdir+image_right, tempdir+pack_folder+pack_icon_name)

class PackingPack:
  old_names = ["Back.png", "Left.png", "Front.png", "Right.png", "Top.png", "Bottom.png"]
  new_names = ["cubemap_0.png", "cubemap_1.png", "cubemap_2.png", "cubemap_3.png", "cubemap_4.png", "cubemap_5.png"]

  def MoveToOut(self, pack_name):
    #? Move the output_image in the output directory
    path_finished = tempdir+pack_name+"\\"
    output_path = configs['Output_Folder'].replace("/", "\\")+"\\"+pack_name
    make_archive(output_path, 'zip', path.dirname(path_finished))
    if pack_name.endswith(".zip") == True: move(output_path+".zip", output_path.replace(".zip", "", 0))
    else: move(output_path+".zip", output_path.replace(".zip", ""))
    return self
  
  def CleanUp(self):
    #! Deletes TEMP files when done or cancel
    print("Cleaning Up '%TEMP%' files")
    if path.exists(tempdir[:-1]):
      rmtree(tempdir[:-1])
      mkdir(tempdir[:-1])
    return self

  def ZipMcpackOrBoth(self, mergejavasky):
    #? Identifies on what your packing choice in the config
    if configs['Convert_To_Zip'] == True: 
      zip_folder = image_details[2]+".zip"
      path_zip = zip_folder+"\\assets\\minecraft\\mcpatcher\\sky\\world0"
      MkJsonPackDetailsFile().makethepackmeta().makepackicon(self.old_names[3], zip_folder, "\\pack.png")
      mergejavasky.save(tempdir+path_zip+'\\'+'cloud1.png')
      for mv_i in range(1,9):
        if not mv_i == 5:
          sky_properties = "sky"+str(mv_i)+".properties"
          copy("resource\\mcpatcher\\sky\\world0\\"+sky_properties, tempdir+path_zip+"\\"+sky_properties)
      self.MoveToOut(zip_folder)

    if configs['Convert_To_Mcpack'] == True: 
      mcpack_folder = image_details[2]+".mcpack"
      path_mcpack = mcpack_folder+"\\textures\\environment\\overworld_cubemap"
      MkJsonPackDetailsFile().makethemanifest().makepackicon(self.old_names[3], mcpack_folder, "\\pack_icon.png")
      for move_no in range (0, 6): 
        sky_names = [self.old_names[move_no], self.new_names[move_no]]
        copy(tempdir+sky_names[0], tempdir+path_mcpack+"\\"+sky_names[1])
      self.MoveToOut(mcpack_folder)
    
    if configs['Convert_To_Zip'] == False and configs['Convert_To_Mcpack'] == False: 
      output_folder = configs['Output_Folder']+"/MC-Sky-Builder/"+strftime("(%b-%d-%Y) %H-%M-%S")
      if path.exists(output_folder): rmtree(output_folder)
      copytree(tempdir, output_folder) 
    return self
