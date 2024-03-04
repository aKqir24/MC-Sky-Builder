import os
import time
import script
import colorama
from colorama import Fore
from gathrr import program

colorama.init()
tempdir = os.getenv('temp')

class mcskyscript(): 

    #========================================#
    # The Program Prepares The Files Needed  #
    #========================================# 

    def imagetocts():
        program.CubeTheSpere()
        os.system('cls')
        print(f"This Script Was Made By {Fore.RED}Akqir{Fore.BLACK}.")
        time.sleep(2)

    # User's Image Input  
    def ImageProperties ():
        imgpath = ""
        while len(imgpath) == 0:
            os.system('cls')
            inpttp0 = (f"Please Input Your Image Location: \n{Fore.GREEN}") 
        #Example - D:\Users\Akqir\Desktop\Documents\sky.jpg
            file = program(input(inpttp0), os.system('cls'))
            imgpath = file.getpath
            file.moveimg()
            program.verfyimgmsg()
        # Verfying Files In User's Input Using The If Statement
            if os.path.exists(tempdir+'\\cspr\\input.jpg'):
                print("Image Has Been Verfied")
                time.sleep(1)
                os.system('cls')
            else:
                print(f"{Fore.RED}Error: [FileNotFoundError] Image Cannot Not Be Verfied!!")
                time.sleep(1)
                os.system('cls')
                solution0 = (" - Choose The Correct File Path Of The Image. \n")
                solution1 = (" - Make Sure The Image Has An .jpg or .bmp extension.")
                print(f"{Fore.WHITE}Possible Solution: \n"+solution0+solution1)
                time.sleep(3.5)
                return mcskyscript.ImageProperties()

    #===========================================================#
    # Image Resolution Of The Output & Output/Path Of The Image #
    #===========================================================#   
    
    def OutputProperties():
        start0=""
        while len(start0) == 0:
            inpttp1 = (f"{Fore.BLACK}Output Folder Of Your Sky Overlay: \n{Fore.GREEN}")
            start0 = input(inpttp1)
            os.system('cls')
            if os.path.exists(start0):
                program.verfyoutputfolder()
                print(f"{Fore.GREEN}Output Folder Verfied{Fore.BLACK}")
                time.sleep(1)
            else:
                program.verfyoutputfolder()
                print(f"{Fore.RED}Error: Output Folder Not Found!!")
                time.sleep(0.7)
                os.system('cls')
                intpttp2 = (f"{Fore.BLACK}Do You Want To Make This Folder In The Current Folder?\n{Fore.GREEN}") 
                ifoutnotfound = input(intpttp2)
                ifoutnotfound = ifoutnotfound.upper()
                if ifoutnotfound == "YES":
                    os.mkdir(start0)
                    time.sleep(0.5)
                    os.system('cls')
                elif ifoutnotfound == "NO":
                    print("Then Please Re-enter The Ouput Folder!!")
                    time.sleep(1)
                    os.system('cls')
                    return mcskyscript.OutputProperties()
                else:
                    print(f"{Fore.RED}Error: Wrong Answer!!{Fore.BLACK}")
                    os.system('cls')
                    time.sleep(1.2)
                    print("The Accepted Value Are Yes & NO")
                    time.sleep(1)
                    os.system('cls')
                    return mcskyscript.OutputProperties()
            try:
                os.system('cls')
                inpttp2 = (f"{Fore.BLACK}Choose Your Desired Resolution:\n{Fore.GREEN}")
                start1 = int(input(inpttp2)) 
                if start1 == 256:
                    script.load()
                    program.puttheimgpath()
                    script.res256() 
                elif start1 == 512:
                    script.load()
                    program.puttheimgpath()
                    script.res512()
                elif start1 == 1024:
                    script.load()
                    program.puttheimgpath()
                    script.res1024()
                elif start1 == 2048:
                    script.load()
                    program.puttheimgpath()
                    script.res2048()
                else:
                    print(f"{Fore.RED}Error: The Input Is Not A Resolution Value!!{Fore.BLACK}")
                    os.system('cls')
                    print("The Accepted Value Are:\n [ 256 512 1024 2048 ]")
            except ValueError:
                print(f"{Fore.RED}Error: [ValueError] Only Numbers Are Allowed!!{Fore.BLACK}")
                time.sleep(1.5)
                os.system('cls')
                print(f"The Accepted Values Are:\n [ 256 512 1024 2048 ] {Fore.BLACK}")
                time.sleep(2.5)
                os.system('cls')
                return mcskyscript.ImageProperties()
    def processing ():
        os.system('cls')
        script.extractall()
        pass
    def finished ():
        pass