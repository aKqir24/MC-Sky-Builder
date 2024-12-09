# This Code Was Made By People From Stackoverflow 
# I Am To Lazy To Make These Kinds Of Hard Code
# Since I'm Just A Beginer I Don't Know Many Maths

from __future__ import print_function
import sys
from all_val import *
from threading import Thread
from math import pi,sin,cos,tan,atan2,hypot,floor
from numpy import clip, hstack, array, concatenate
from worker import PackingPack, Image, ImageTk, _tkinter, messagebox
     
class CreateCubeIMG:
  def __init__(self, progresswindow, create_process, percentage):
    self.percentage = percentage
    self.progresswindow = progresswindow  
    self.create_process = create_process
    
  noimagehandler = lambda self: ConvertDetails.getimageError(self)

  def loadingtitle(self):
    # Update the title of the progress window during loading
    try:
      sleep(1)
      while int(str(self.percentage.get().replace("%", ""))) < 100:
        for tlno in range(0, 7):
          if int(str(self.percentage.get().replace("%", ""))) >= 99: 
            self.progresswindow.destroy()
            messagebox.showinfo(title="Finished!!", message="Sky `Building` was a success :D")
            break
          else:
            sleep(1)
            titlemsg = ("Building Sky")
            titledot = [ " ",".","."*2,"."*3, "."*3, "."*2, "." ]
            self.progresswindow.title(titlemsg+titledot[0+tlno])
    except _tkinter.TclError: pass
    except RuntimeError: pass
    except ValueError: pass
  
  def mergeskyedges(self, correct_position, blend_width):
    # Merge sky edge images into a single image to blend the pixels
    top = Image.open(tempdir+'Top'+ext).rotate(-180)
    front = Image.open(tempdir+'Front'+ext)
    bottom = Image.open(tempdir+'Bottom'+ext).rotate(180)
    mrg = Image.new("RGBA", (top.size[0], top.size[0]*3))
    mrg.paste(top)
    mrg.paste(front, (0, top.size[0]))
    mrg.paste(bottom, (0, front.size[0]*2))
    left = mrg.crop((0, 0, front.width // 2, top.height*3))
    right = mrg.crop((top.width // 2, 0, top.width, top.height*3))
    combined = Image.fromarray(concatenate((array(left), array(right)),axis=1))
    for alpi in range(blend_width): 
      alpha = alpi / blend_width
      for bl in range(top.height*3):
        #if alpi < curve_radius: alpha = (alpi + 1) / curve_radius
        x1 = max(0, min(left.width - 1, left.width - blend_width + alpi))
        x2 = max(0, min(right.width - 1, blend_width - alpi))
        pixel1, pixel2 = [(left.getpixel((x1, bl))), (right.getpixel((x2, bl)))]
        blended_pixel = tuple(int((1 - alpha) * a + alpha * b) for a, b in zip(pixel1, pixel2))        
        combined.putpixel((top.width // 2 - blend_width + alpi + correct_position, bl), blended_pixel)
    return combined

  def mergejavasky(self):
    filenames = PackingPack.old_names
    temp_images = [
      Image.open(tempdir + filenames[5]),  # bottom
      Image.open(tempdir + filenames[4]),  # top
      Image.open(tempdir + filenames[0]),  # back
      Image.open(tempdir + filenames[1]),  # left
      Image.open(tempdir + filenames[2]),  # front
      Image.open(tempdir + filenames[3]) ] # right

    # Create a new image with appropriate size
    width, height = temp_images[0].size
    javasky = Image.new("RGBA", (width * 3, height * 2))
    # Paste images into the new image
    for img_i, temp_image in enumerate(temp_images):
      
      # Top row (bottom, top, back)
      if img_i < 3: x_offset, y_offset = [(width * img_i), 0]
      # Bottom row (left, front, right)
      else: x_offset, y_offset = [(width * (img_i - 3)), height] 
      javasky.paste(temp_image, (int(x_offset), int(y_offset)))
    return javasky
      
  def getcreatesky(self):
    def cropmergedimage(old_names, save_merged):
    # Crop the blended merged image into three parts & save them
      merged_image = Image.open(save_merged)
      coords = [
        (0, 0, img_res, img_res),             
        (0, img_res, img_res, img_res * 2),    
        (0, img_res * 2, img_res, img_res * 3) ]
      
      for i ,croped_coords in enumerate(coords):
        name_index = [4, 2, 5]
        indexed_names = tempdir+old_names[name_index[i]]
        cropped_img = merged_image.crop(croped_coords)
        rm(indexed_names)
        if i == 2: 
          print("Yes")
          cropped_img.rotate(180).save(indexed_names)
        else: cropped_img.save(indexed_names)
      rm(save_merged)

    try:
      self.progresswindow.focus_set()
      imgIn = Image.open(image_details[0]) 
      inSize = imgIn.size 
      imgOut = Image.new("RGB",(inSize[0],int(inSize[0]*3/4)),"black")
      # Set the progress_bar parameters based on input image size
      if inSize[0] >= 3840 or inSize[1] >= 2160: pv, correct_position, blend_width = [0.010, 4, 55]
      elif inSize[0] >= 2048 or inSize[1] >= 1080 : pv, correct_position, blend_width = [0.0225, 3, 50]
      elif inSize[0] >= 1280 or inSize[1] >= 1080 : pv, correct_position = [0.045, 3, 46]
      else: pv, correct_position, blend_width = [0.071, 2, 42]
      createcube = ConvertDetails( imgIn, imgOut, self.progresswindow, self.create_process, self.percentage, pv)
      progress_value, packsky = [(createcube.convertBack()),(PackingPack)]
      
      name_map = [ \
           ["", "", "Top", ""],
           ["Front", "Right", "Back", "Left"],
           ["", "", "Bottom", ""]]

      width, height = imgOut.size 
      save_merged = tempdir+'combined.png'
      img_res, out_path, cube_size = [(readconfig()[0]), (readconfig()[1]), (width/4)]
      for row in range(3):
        for col in range(4):
          createcube.CurrentProgress(progress_value)
          if name_map[row][col] != "":
            sx, sy, fn = [(cube_size * col), (cube_size * row), (name_map[row][col] + '.png')]
            imgOut.crop((sx, sy, sx + cube_size, sy + cube_size)).resize((int(img_res), int(img_res))).save(tempdir+fn)
      get_remaining_progress = 100-progress_value
      divide_remaining_progress = get_remaining_progress/3
      for remaining_process in range(1,5):
        if remaining_process == 4: sleep(1)
        else:
          createcube.CurrentProgress(progress_value+divide_remaining_progress*remaining_process)
          if remaining_process == 1: self.mergeskyedges(correct_position, blend_width).save(save_merged)
          if remaining_process == 2: cropmergedimage(packsky.old_names, save_merged)
          if remaining_process == 3: packsky().ZipMcpackOrBoth(self.mergejavasky()).CleanUp()
    except IndexError: self.noimagehandler()
    except _tkinter.TclError: pass

class ConvertDetails(CreateCubeIMG):
  def __init__ (self, imgIn, imgOut, progresswindow, create_process, percentage, pv):
    super().__init__(progresswindow, create_process, percentage)
    self.imgIn = imgIn
    self.imgOut = imgOut
    self.pv = pv

  def outImgToXYZ(i,j,face,edge):
    a, b = [(2.0*float(i)/edge), (2.0*float(j)/edge)]
    # Calculate coordinates based on the face of the cube
    if face==0: (x,y,z) = (-1.0, 1.0-a, 3.0 - b)    # back
    elif face==1: (x,y,z) = (a-3.0, -1.0, 3.0 - b)  # left
    elif face==2: (x,y,z) = (1.0, a - 5.0, 3.0 - b) # front
    elif face==3: (x,y,z) = (7.0-a, 1.0, 3.0 - b)   # right
    elif face==4: (x,y,z) = (b-1.0, a -5.0, 1.0)    # top
    elif face==5: (x,y,z) = (5.0-b, a-5.0, -1.0)    # bottom
    return (x,y,z)

  def convertBack(self):
    inSize, outSize = [(self.imgIn.size), (self.imgOut.size)]
    inPix, outPix = [(self.imgIn.load()), (self.imgOut.load())]
    edge = inSize[0]/4   # the length of each edge in pixels
    current_percent = 1
    for i in range(outSize[0]):
      face = int(i/edge) # 0 - back, 1 - left 2 - front, 3 - right
      if face==2: rng = range(0,int(edge*3))
      else: rng = range(int(edge), int(edge) * 2)
      current_percent = self.CurrentProgress(current_percent)
      for j in rng:
        if j<edge: face2 = 4      # top
        elif j>=2*edge: face2 = 5 # bottom
        else: face2 = face
        (x,y,z) = ConvertDetails.outImgToXYZ(i,j,face2,edge)
        theta, r = [(atan2(y,x)), (hypot(x,y))] # range -pi to pi
        phi = atan2(z,r)                        # range -pi/2 to pi/2
        # source img coords
        uf = ( 2*edge*(theta + pi)/pi )
        vf = ( 2.14*edge * (pi/1.869 - phi)/pi)
        # Use bilinear interpolation between the four surrounding pixels
        ui, vi = [(floor(uf)),(floor(vf))]  # coord of pixel to bottom left
        u2, v2 = [(ui+1),(vi+1)]            # coords of pixel to top right     
        mu, nu = [(uf-ui), (vf-vi)]         # fraction of way across pixel
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
    return current_percent

  def CurrentProgress(self, current_percent):
    percent_interval = self.pv
    pross_interval = current_percent+percent_interval
    current_percent = pross_interval
    self.percentage.set(str(int(current_percent))+"%")
    self.create_process['value']=current_percent
    self.progresswindow.update_idletasks()
    return current_percent

  def getimageError(self):
    # Handle image opening errors
    self.progresswindow.destroy()
    errormessage = "Image file is not opened or found"
    messagebox.showerror( title="Error_2", message=errormessage)
    return self