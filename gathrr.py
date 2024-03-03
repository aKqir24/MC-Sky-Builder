#GOD is Good All The Time 
import os
import time
import glob
import shutil
import keyboard

tempdir = os.getenv('TEMP')

class program():
    def installrequirements ():
        os.system("color f0")
        os.system("pip install keyboard")
        os.system("pip install colorama")
        
#======================================#
# The Program Start To Inroduce Itself #
#======================================#

    def firstlaunch():  
        text1 = ("Hello User, Thank You For Downloading My Script!!")
        time.sleep(0.5)
        os.system('cls')
        print("Starting.")
        time.sleep(0.5)
        os.system('cls')
        print("Starting..")
        time.sleep(0.5)
        os.system('cls')
        print("Starting...")
        time.sleep(0.5)
        os.system('cls')
        print("Starting.")
        time.sleep(0.5)
        os.system('cls')
        print("Starting..")
        time.sleep(0.5)
        os.system('cls')
        print("Starting...")
        time.sleep(0.5)
        os.system('cls')
        print("Done!!")
        os.system('cls')
        print (text1)
        time.sleep(3)  

#===============================================#
# Gets The Image Path By Using The User's Input #
#===============================================#

    def __init__(self, getpath, clearcmd):
        self.getpath = getpath
        self.clearcmd = clearcmd
    def puttheimgpath ():
        keyboard.write(tempdir+'\\cspr\\input.jpg')
        #imgsource='/Users/Akqir/Desktop/Documents/*.bmp'

#=========================================#       
# Putting & Opening The CubeShpereProgram #
#=========================================#

    def CubeTheSpere():
        if os.path.exists(tempdir+'\\cspr'):
            shutil.rmtree(tempdir+'\\cspr')
            shutil.copytree('cspr', tempdir+'\\cspr')
        else:
            shutil.copytree('cspr', tempdir+'\\cspr')

    
    def moveimg(self):
        try:
            imgsource = self.getpath
            # retrieve file list
            filelist=glob.glob(imgsource)
            for img in filelist:
                 # move file with full paths as shutil.move() parameters
                shutil.copy(img,tempdir+'\\cspr\\input.jpg')       
        # Verfying Files In User's Input By Handling Exceptions
        except FileNotFoundError:
            print("Error: [FileNotFoundError] Image Cannot Not Be Verfied!!")
            time.sleep(0.5)
            solution0 = (" - Choose The Correct File Path Of The Image. \n")
            solution1 = (" - Make Sure The Image Has An .jpg or .bmp extension. \n")
            print("Possible Solution: \n"+solution0+solution1)

    #======================================#
    # The Verifying File & Folder Messages #
    #======================================# 
    
    def verfyimgmsg():
        verfyimg = ("Verifiying File.")
        time.sleep(0.4)
        print(str(verfyimg))
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'.')
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'..')
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'...')
        os.system('cls')
        time.sleep(0.4)

    def verfyoutputfolder():
        verfyout = ("Verifiying Output Folder.")
        time.sleep(0.4)
        print(str(verfyout))
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'.')
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'..')
        time.sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'...')
        os.system('cls')
        time.sleep(0.4)