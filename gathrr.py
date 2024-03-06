#GOD is Good All The Time 
import os
import glob
import colorama
from colorama import Fore
from time import sleep
from shutil import copytree,_rmtree_unsafe,copy

tempdir = os.getenv('TEMP')

class program():
        
#======================================#
# The Program Start To Inroduce Itself #
#======================================#

    def firstlaunch():  
        text1 = (f"{Fore.BLACK}Hello User, Thank You For Downloading My Script!!")
        sleep(0.5)
        os.system('cls')
        print("Starting.")
        sleep(0.5)
        os.system('cls')
        print("Starting..")
        sleep(0.5)
        os.system('cls')
        print("Starting...")
        sleep(0.5)
        os.system('cls')
        print("Starting.")
        sleep(0.5)
        os.system('cls')
        print("Starting..")
        sleep(0.5)
        os.system('cls')
        print("Starting...")
        sleep(0.5)
        os.system('cls')
        print("Done!!")
        os.system('cls')
        print (text1)
        sleep(2)
        os.system('cls')
        print(f"This Script Was Made By {Fore.RED}Akqir{Fore.BLACK}.")
        sleep(3)  

#===============================================#
# Gets The Image Path By Using The User's Input #
#===============================================#

    def __init__(self, getpath, clearcmd):
        self.getpath = getpath
        self.clearcmd = clearcmd
    
        #imgsource='/Users/Akqir/Desktop/Documents/*.bmp'

#=========================================#       
# Putting & Opening The CubeShpereProgram #
#=========================================#
    def makethetempdir ():
        if os.path.exists(tempdir+'\\cspr'):
            _rmtree_unsafe(tempdir+'\\cspr', next)
            os.mkdir(tempdir+'\\cspr')
        else:
            os.mkdir(tempdir+'\\cspr')

    
    def moveimg(self):
        try:
            imgsource = self.getpath
            # retrieve file list
            filelist=glob.glob(imgsource)
            for img in filelist:
                 # copy file with full paths as copy() parameters
                copy(img,tempdir+'\\cspr\\input.jpg')       
        # Verfying Files In User's Input By Handling Exceptions
        except FileNotFoundError:
            print("Error: [FileNotFoundError] Image Cannot Not Be Verfied!!")
            sleep(0.5)
            solution0 = (" - Choose The Correct File Path Of The Image. \n")
            solution1 = (" - Make Sure The Image Has An .jpg or .bmp extension. \n")
            print("Possible Solution: \n"+solution0+solution1)

    #======================================#
    # The Verifying File & Folder Messages #
    #======================================# 
    
    def verfyimgmsg():
        verfyimg = ("Verifiying File.")
        sleep(0.4)
        print(str(verfyimg))
        sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'.')
        sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'..')
        sleep(0.4)
        os.system('cls')
        print(str(verfyimg)+'...')
        os.system('cls')
        sleep(0.4)

    def verfyoutputfolder():
        verfyout = ("Verifiying Output Folder.")
        sleep(0.4)
        print(str(verfyout))
        sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'.')
        sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'..')
        sleep(0.4)
        os.system('cls')
        print(str(verfyout)+'...')
        os.system('cls')
        sleep(0.4)

