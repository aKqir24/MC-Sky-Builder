"""
    
    Fetches the conversion details & does it with create.py

"""
from create import CreateCubeIMG
from tkinter import messagebox
from os import remove as rm
from config import *

class ConvertDetails(CreateCubeIMG):
  def __init__ (self, imgIn, imgOut, progresswindow, create_process, percentage):
    super().__init__(progresswindow, create_process, percentage)
    self.imgIn = imgIn
    self.imgOut = imgOut

  def outImgToXYZ(i,j,face,edge):
    a, b = [(2.0*float(i)/edge), (2.0*float(j)/edge)]
    # Calculate coordinates based on the face of the cube
    match face:
        case 0: (x,y,z) = (-1.0, 1.0-a, 3.0 - b)  # back
        case 1: (x,y,z) = (a-3.0, -1.0, 3.0 - b)  # left
        case 2: (x,y,z) = (1.0, a - 5.0, 3.0 - b) # front
        case 3: (x,y,z) = (7.0-a, 1.0, 3.0 - b)   # right
        case 4: (x,y,z) = (b-1.0, a -5.0, 1.0)    # top
        case 5: (x,y,z) = (5.0-b, a-5.0, -1.0)    # bottom
    return (x,y,z)

  def convertBack(self, pv):
    inSize, outSize = [(self.imgIn.size), (self.imgOut.size)]
    inPix, outPix = [(self.imgIn.load()), (self.imgOut.load())]
    edge = inSize[0]/4   # the length of each edge in pixels
  
    def convertprocess():
      current_percent = 1
      for i in range(outSize[0]):
        face = int(i/edge) # 0 - back, 1 - left 2 - front, 3 - right
        if face==2: rng = range(0,int(edge*3))
        else: rng = range(int(edge), int(edge) * 2)
        current_percent = self.CurrentProgress(pv ,current_percent)
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
      process=Thread(target=convertprocess, args=(pv, current_percent))
      process.daemon = True
      process.start()
      
  def CurrentProgress(self, pv, current_percent):
    print(current_percent+ pv)
    pross_interval = current_percent+pv
    current_percent = pross_interval
    self.percentage.set(str(int(current_percent))+"%")
    self.create_process.set(current_percent / 100.0)
    self.progresswindow.update_idletasks()
    return current_percent

  def OutputValues(self, inSize):
    # Set the progress_bar parameters based on input image size
    if inSize[0] >= 3840 or inSize[1] >= 2160: pv, correct_position, blend_width = [0.010, 6, 55]
    elif inSize[0] >= 2048 or inSize[1] >= 1080 : pv, correct_position, blend_width = [0.0225, 4, 50]
    elif inSize[0] >= 1280 or inSize[1] >= 1080 : pv, correct_position = [0.045, 3, 46]
    else: pv, correct_position, blend_width = [0.071, 2, 42]
    return [pv, correct_position, blend_width]
