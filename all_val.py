"""

  Distributes the ''Elements'' used, in the modules

""" 

from os import getenv

dsktp_regkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
font_details = [('Noto Sans',8,'normal'), ('Segoe UI',10,'normal')] 
config_dir = getenv('APPDATA')+'\\mcskymaker\\settings.json' 
tempdir = getenv('TEMP')+'\\cspr\\'
image_details = []
rel = 'flat'

# color scheme
db, b, b2, f, ab = [ "#283149","#404b69", "#333e5f", "#dbedf3", "#00818a" ]
# place coords
yp, x, y , yb = [ 225, 15, 3, 2 ]