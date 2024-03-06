import os
import colorama
from time import sleep
from colorama import Fore
from gathrr import program
from keyboard import write, press_and_release


colorama.init()
program.makethetempdir()
tempdir = os.getenv('temp')

class mcskyscript(): 

    #========================================#
      #
    #========================================# 

    def imagetocts():
        os.system('cls')
        print(f"This Script Was Made By {Fore.RED}Akqir{Fore.BLACK}.")
        sleep(2)

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
                sleep(1)
                os.system('cls')
            else:
                print(f"{Fore.RED}Error: [FileNotFoundError] Image Cannot Not Be Verfied!!")
                sleep(1)
                os.system('cls')
                solution0 = (" - Choose The Correct File Path Of The Image. \n")
                solution1 = (" - Make Sure The Image Has An .jpg or .bmp extension.")
                print(f"{Fore.WHITE}Possible Solution: \n"+solution0+solution1)
                sleep(3.5)
                return mcskyscript.ImageProperties()

    #========================================#
    # Output Image Properies And Output Path #
    #========================================#   
    
    def OutputProperties():
        start0=""
        while len(start0) == 0:
            inpttp1 = (f"{Fore.BLACK}Output Folder Of Your Sky Overlay: \n{Fore.GREEN}")
            start0 = input(inpttp1)
            os.system('cls')
            if os.path.exists(start0):
                program.verfyoutputfolder()
                print(f"{Fore.GREEN}Output Folder Verfied{Fore.BLACK}")
                sleep(1)
            else:
                program.verfyoutputfolder()
                print(f"{Fore.RED}Error: Output Folder Not Found!!")
                sleep(0.7)
                os.system('cls')
                intpttp2 = (f"{Fore.BLACK}Do You Want To Make This Folder In The Current Folder?\n{Fore.GREEN}") 
                ifoutnotfound = input(intpttp2)
                ifoutnotfound = ifoutnotfound.upper()
                if ifoutnotfound == "YES":
                    os.mkdir(start0)
                    sleep(0.5)
                    os.system('cls')
                elif ifoutnotfound == "NO":
                    os.system('cls')
                    print(f"{Fore.BLACK}Then Please Re-enter The Ouput Folder!!")
                    sleep(1)
                    os.system('cls')
                    return mcskyscript.OutputProperties()
                else:
                    print(f"{Fore.RED}Error: Wrong Answer!!{Fore.BLACK}")
                    os.system('cls')
                    sleep(1.2)
                    print("The Accepted Value Are Yes & NO")
                    sleep(1)
                    os.system('cls')
                    return mcskyscript.OutputProperties()            
    # Output Resolution Image
        try:
            os.system('cls')
            inpttp2 = (f"{Fore.BLACK}Choose Your Desired Resolution:\n{Fore.GREEN}")
            start1 = int(input(inpttp2)) 
            if start1 == 256:
                os.startfile("cspr\\cube_256.py")
                press_and_release('Winodows+Down')
            elif start1 == 512:
                os.startfile("cspr\\cube_512.py")
                press_and_release('Winodows+Down')
            elif start1 == 1024:
                os.startfile("cspr\\cube_1024.py")
                press_and_release('Winodows+Down')
            elif start1 == 2048:
                os.startfile("cspr\\cube_2048.py")
                press_and_release('Winodows+Down')
            else:
                os.system('cls')
                print(f"{Fore.RED}Error: The Input Is Not A Resolution Value!!{Fore.BLACK}")
                os.system('cls')
                print("The Accepted Value Are:\n [ 256 512 1024 2048 ]")
        except ValueError:
                os.system('cls')
                print(f"{Fore.RED}Error: [ValueError] Only Numbers Are Allowed!!{Fore.BLACK}")
                sleep(1.5)
                os.system('cls')
                print(f"The Accepted Values Are:\n [ 256 512 1024 2048 ] {Fore.BLACK}")
                sleep(2.5)
                os.system('cls')
                return mcskyscript.OutResolution()
    def processing ():
        pass
    def finished ():
        pass