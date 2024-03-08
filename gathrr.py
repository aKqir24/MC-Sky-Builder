#GOD is Good All The Time 
import colorama
from glob import glob
from time import sleep
from colorama import Fore
from os import path,getenv,system,mkdir
from shutil import copytree,_rmtree_unsafe,copy

sleepval = float(0.43)
tempdir = getenv('TEMP')

class program():
        
#======================================#
# The Program Start To Inroduce Itself #
#======================================#

    def firstlaunch():
        system('color f0')  
        text1 = (f"{Fore.BLACK}Hello User, Thank You For Downloading My Script!!")
        sleep(0.5)
        system('cls')
        starting= ""
        for startingmsg in range(0, 3):
            strtmsg = ("Starting")
            strtend = [ ".","."*2,"."*3 ]
            startingmsg = ( print(strtmsg+strtend[0]), sleep(sleepval), system('cls'),
                            print(strtmsg+strtend[1]), sleep(sleepval), system('cls'),
                            print(strtmsg+strtend[2]), sleep(sleepval), system('cls'))
        print(f"This Script Was Made By {Fore.RED}Akqir{Fore.BLACK}.")
        sleep(3)  
# Gets The Image Path By Using The User's Input #
    def __init__(self, getpath, clearcmd):
        self.getpath = getpath
        self.clearcmd = clearcmd
        #imgsource='/Users/Akqir/Desktop/Documents/*.bmp'
        
#========================================#       
# Moving & Preparing The Files Directory #
#========================================#
    def makethetempdir ():
        if path.exists(tempdir+'\\cspr'):
            _rmtree_unsafe(tempdir+'\\cspr', next)
            mkdir(tempdir+'\\cspr')
        else:
            mkdir(tempdir+'\\cspr')
    
    def moveimg(self):
        try:
            imgsource = self.getpath
            # retrieve file list
            filelist=glob(imgsource)
            for img in filelist:
                 # copy file with full paths as copy() parameters
                copy(img,tempdir+'\\cspr\\input.jpg')       
        # Verfying Files In User's Input By Handling Exceptions
        except FileNotFoundError:
            print(f"{Fore.RED}Error: [FileNotFoundError] Image Cannot Not Be Verfied!!{Fore.BLACK}")
            sleep(0.5)
            solution0 = (" - Choose The Correct File Path Of The Image. \n")
            solution1 = (" - Make Sure The Image Has An .jpg or .bmp extension.")
            print("Possible Solution: \n"+solution0+solution1)

    #======================================#
    # The Verifying File & Folder Messages #
    #======================================# 
    
    def verfyimgmsg():
        fileverloca= ""
        for fileverloca in range(0, 3):
            verfmsg = ("Verifying File")
            verfend = [ ".","."*2,"."*3 ]
            fileverloca = ( print(verfmsg+verfend[0]), sleep(sleepval), system('cls'),
                            print(verfmsg+verfend[1]), sleep(sleepval), system('cls'),
                            print(verfmsg+verfend[2]), sleep(sleepval), system('cls'))

    def verfyoutputfolder():
        verfoutfold= ""
        for fileverf in range(0, 3):
            verfoutmsg = ("Verifying File")
            verfoutend = [ ".","."*2,"."*3 ]
            verfoutfold = ( print(verfoutmsg+verfoutend[0]), sleep(sleepval), system('cls'),
                            print(verfoutmsg+verfoutend[1]), sleep(sleepval), system('cls'),
                            print(verfoutmsg+verfoutend[2]), sleep(sleepval), system('cls'))