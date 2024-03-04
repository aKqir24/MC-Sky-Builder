# This Code Was Made By People From Stackoverflow 
# I Am To Lazy To Make These Kinds Of Hard Code
# Since I'm Just A Beginer I Don't Know Many Maths

from __future__ import print_function
import sys
from time import sleep
from numpy import clip
from json import load, dump
from threading import Thread
from math import pi,sin,cos,tan,atan2,hypot,floor
from worker import MkJsonPackDetailsFile, _tkinter, messagebox, Image, ImageTk,  tempdir, config_dir
     
class CreateCubeIMG:
  def __init__(self, progresswindow, create_process, percentage):
    self.percentage = percentage
    self.progresswindow = progresswindow  
    self.create_process = create_process
    
  def loadingtitle(self):
    try:
      sleep(1)
      while int(str(self.percentage.get().replace("%", ""))) <= 100:
        if int(str(self.percentage.get().replace("%", ""))) >= 99: 
          self.progresswindow.title("Done!!")
          break
        for tlno in range(0, 7):
          sleep(1)
          titlemsg = ("Building Sky")
          titleldng = [ " ",".","."*2,"."*3, "."*3, "."*2, "." ]
          self.progresswindow.title(titlemsg+titleldng[0+tlno])   
    except RuntimeError: pass
    except ValueError: pass
  
  def mergeskyedges():
    ext = image_details[1]
    top = Image.open(tempdir+'Top'+ext).rotate(-180)
    front = Image.open(tempdir+'Front'+ext)
    bottom = Image.open(tempdir+'Bottom'+ext).rotate(180)
    mrg = Image.new("RGBA", (top.size[0], top.size[0]*3))
    mrg.paste(top)
    mrg.paste(front, (0, top.size[0]))
    mrg.paste(bottom, (0, front.size[0]*2))
    return mrg
    
  def getimageError(self):
    self.progresswindow.destroy()
    errormessage = "Image file is not opened or found"
    messagebox.showerror( title="Error_2", message=errormessage)
      
  def getcreatesky(self):
    try:
      self.progresswindow.focus_set()
      imgIn = Image.open(image_details[0])
      inSize = imgIn.size
      self.create_process.config(value=1)
      imgOut = Image.new("RGB",(inSize[0],int(inSize[0]*3/4)),"black")
      createcube = ConvertDetails( imgIn, imgOut , self.progresswindow, self.create_process, self.percentage)
      createcube.convertBack()
      
      name_map = [ \
           ["", "", "Top", ""],
           ["Front", "Right", "Back", "Left"],
           ["", "", "Bottom", ""]]
      
      with open(config_dir, 'r') as readconfig:
        readusingjson = load(readconfig)
        img_res = readusingjson['Image_Size']
        out_path = readusingjson['Outputfolder_Path']
        width, height = imgOut.size
        cube_size = width/4
        for row in range(3):
          for col in range(4):
            if name_map[row][col] != "":
              sx = cube_size * col
              sy = cube_size * row
              fn = name_map[row][col] + '.png'
              imgOut.crop((sx, sy, sx + cube_size, sy + cube_size)).resize((int(img_res), int(img_res))).save(tempdir+fn)
              self.create_process.config(value=100)
              self.percentage.set(str("100%"))
        CreateCubeIMG.mergeskyedges().save(tempdir+'unconnected.png')
    except IndexError: CreateCubeIMG.getimageError(self)
    except _tkinter.TclError: pass

class ConvertDetails(CreateCubeIMG):
    def __init__ (self, imgIn, imgOut, progresswindow, create_process, percentage):
      super().__init__(progresswindow, create_process, percentage)
      self.imgIn = imgIn
      self.imgOut = imgOut

    def outImgToXYZ(i,j,face,edge):
      a = 2.0*float(i)/edge
      b = 2.0*float(j)/edge
      if face==0: (x,y,z) = (-1.0, 1.0-a, 3.0 - b) # back
      elif face==1: (x,y,z) = (a-3.0, -1.0, 3.0 - b) # left
      elif face==2: (x,y,z) = (1.0, a - 5.0, 3.0 - b) # front
      elif face==3: (x,y,z) = (7.0-a, 1.0, 3.0 - b) # right
      elif face==4: (x,y,z) = (b-1.0, a -5.0, 1.0)# top
      elif face==5: (x,y,z) = (5.0-b, a-5.0, -1.0) # bottom
      return (x,y,z)

    def convertBack(self):
      inSize = self.imgIn.size
      outSize = self.imgOut.size
      inPix = self.imgIn.load()
      outPix = self.imgOut.load()
      edge = inSize[0]/4   # the length of each edge in pixels
      current_percent = 1
      for i in range(outSize[0]):
          pross_interval = current_percent+0.045
          current_percent = pross_interval
          self.percentage.set(str(int(current_percent))+"%")
          self.create_process['value']+=0.045
          self.progresswindow.update_idletasks()
          face = int(i/edge) # 0 - back, 1 - left 2 - front, 3 - right
          if face==2: rng = range(0,int(edge*3))
          else: rng = range(int(edge), int(edge) * 2)
          for j in rng:
              if j<edge: face2 = 4 # top
              elif j>=2*edge: face2 = 5 # bottom
              else: face2 = face
              (x,y,z) = ConvertDetails.outImgToXYZ(i,j,face2,edge)
              theta = atan2(y,x) # range -pi to pi
              r = hypot(x,y)
              phi = atan2(z,r) # range -pi/2 to pi/2
              # source img coords
              uf = ( 2*edge*(theta + pi)/pi )
              vf = ( 2.14*edge * (pi/1.869 - phi)/pi)
              # Use bilinear interpolation between the four surrounding pixels
              ui = floor(uf)  # coord of pixel to bottom left
              vi = floor(vf)
              u2 = ui+1       # coords of pixel to top right
              v2 = vi+1       
              mu = uf-ui      # fraction of way across pixel
              nu = vf-vi
              A = inPix[ui % inSize[0],int(clip(vi,0,inSize[1]-1))]
              B = inPix[u2 % inSize[0],int(clip(vi,0,inSize[1]-1))]
              C = inPix[ui % inSize[0],int(clip(v2,0,inSize[1]-1))]
              D = inPix[u2 % inSize[0],int(clip(v2,0,inSize[1]-1))]
              # interpolate
              (r,g,b) = (
                A[0]*(1-mu)*(1-nu) + B[0]*(mu)*(1-nu) + C[0]*(1-mu)*nu+D[0]*mu*nu,
                A[1]*(1-mu)*(1-nu) + B[1]*(mu)*(1-nu) + C[1]*(1-mu)*nu+D[1]*mu*nu,
                A[2]*(1-mu)*(1-nu) + B[2]*(mu)*(1-nu) + C[2]*(1-mu)*nu+D[2]*mu*nu )
              outPix[i,j] = (int(round(r)),int(round(g)),int(round(b)))