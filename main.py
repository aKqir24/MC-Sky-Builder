import os
import colorama
from time import sleep
from colorama import Fore
from gathrr import program
from tkinter import filedialog,PhotoImage,Label
from keyboard import write, press_and_release

colorama.init()
program.makethetempdir()
tempdir = os.getenv('TEMP')
userdir = os.getenv('USERNAME')
logo = PhotoImage(file='res/icon.png')

class mcskyscript(): 
    
    #====================#
    # User's Image Input # 
    #====================#
    
    def ImageProperties ():
        try:
            os.system('cls')
            print(f"{Fore.BLACK}Choose Your Image Directory:")
            inpttp0 = filedialog.askopenfilename( initialdir=userdir, 
                                                  title="Image File", 
                                                  filetypes=(("Image Files","*.jpg *.png"),
                                                            ("Image Files","*.jpg *.png")))
        #Example - D:\Users\Akqir\Desktop\Documents\sky.jpg
            imglocation = open(inpttp0, 'r')
            file = program(imglocation.name, os.system('cls'))
            imgpath = file.getpath
            file.moveimg()
        # Verfying Files In User's Input Using The If Statement
            if os.path.exists(tempdir+'\\cspr\\input.jpg'):
                program.verfyimgmsg()
                print(f"{Fore.GREEN}Image Has Been Verfied{Fore.BLACK}")
                sleep(1)
                os.system('cls')
        except FileNotFoundError:
            os.system('cls')
            program.verfyimgmsg()
            print(f"{Fore.RED}Error: [FileNotFoundError] Image Cannot Not Be Verfied!!")
            sleep(1)
            os.system('cls')
            solution0 = (" - Choose The Correct File Path Of The Image. \n")
            solution1 = (" - Make Sure The Image Has An .jpg or .png extension.")
            print(f"{Fore.WHITE}Possible Solution: \n"+solution0+solution1)
            sleep(3.5)
            return mcskyscript.ImageProperties()

    #========================================#
    # Output Image Properies And Output Path #
    #========================================#   
    
    def OutputProperties():
        print(f"{Fore.BLACK}Pick The Output Folder:")
        inpttp1 = filedialog.askdirectory(initialdir=userdir, title="Output Folder",)
        os.system('cls')
        if os.path.exists(inpttp1):
            program.verfyoutputfolder()
            print(f"{Fore.GREEN}Output Folder Verfied{Fore.BLACK}")
            sleep(1)
        else:
            program.verfyoutputfolder()
            print(f"{Fore.RED}Error: Output Folder Not Found!!")
            sleep(0.7)
            os.system('cls')
            ifoutnotfound = input(f"{Fore.BLACK}Create This Folder In The Program's Folder?\n{Fore.GREEN}")
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
                erroran = ( print(f"{Fore.RED}Error: Wrong Answer!!{Fore.BLACK}"), os.system('cls'),
                            sleep(1.2), print("The Accepted Value Are Yes & NO"), sleep(1), os.system('cls'))
                return mcskyscript.OutputProperties()    
            
    # Output Resolution Image
        try:
            os.system('cls')
            start1 = int(input(f"{Fore.BLACK}Choose Your Desired Resolution:\n{Fore.GREEN}")) 
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
                errorwintpu = ( os.system('cls'), print(f"{Fore.RED}Error: The Input Is Not In The List Of Supported Resolution!!{Fore.BLACK}"),
                                os.system('cls'), print(f"The Accepted Value Are: [ 256 512 1024 2048 ] {Fore.BLACK}"))
        except ValueError:
                errorwvalue = ( os.system('cls'), print(f"{Fore.RED}Error: [ValueError] Only Numbers Are Allowed!!{Fore.BLACK}"),
                                sleep(1.5), os.system('cls'),print(f"The Accepted Values Are: [ 256 512 1024 2048 ] {Fore.BLACK}"),
                                sleep(2.5),os.system('cls'))
                return mcskyscript.OutputProperties()

    def processing ():
        pass
    def finished ():
        pass