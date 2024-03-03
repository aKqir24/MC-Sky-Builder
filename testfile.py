import os
#import glob
#import shutil
#
## I prefer to set path and mask as variables, but of course you can use values
## inside glob() and move()
#
#imgsource='/Users/Akqir/Desktop/Documents/*.bmp'
#target_folder='/Users/Akqir/Desktop/Documents/Projects'
#
## retrieve file list
#filelist=glob.glob(imgsource)
#for single_file in filelist:
#     # move file with full paths as shutil.move() parameters
#    shutil.move(single_file,target_folder) 
#temp = os.getenv('TEMP')
#print(temp+'')

intpttp2 = ("Do You Want To Make This Folder In The Current Folder?\n") 
ifoutnotfound = input(intpttp2)
ifoutnotfound = ifoutnotfound.upper()
if ifoutnotfound == "YES":
    print("OK")
elif ifoutnotfound == "NO":
    print("HEEE")