 # At First I will GOD is Good All The Time :) #
from all_val import *
from tkinter import Tk, Button
from tkinter.ttk import Progressbar
from subprocess import Popen as showfolder, run
from worker import GetImageDetails, filedialog, Toplevel, Label, StringVar
from settings import SettingsWindow, Frame, BooleanVar, Thread, Image, ImageTk, CreateCubeIMG, load, resetto, _tkinter

resetto().makethetempdir().setdefaults()

# mainwindow ( Main Window Of The Program )
mainwindow = Tk()
mainwindow.geometry('374x266')
mainwindow.title("MC Sky Builder")
mainwindow.config(background="#283149")
mainwindow.iconbitmap('res\\icon.ico')
mainwindow.resizable(False, False)

# mainwindow ( Labels/Frames Of The Path & Location )
Imageinput = Label( mainwindow, text="Image Folder :", bg="#283149", fg=f, pady= 1, bd=0 )
Fileprevb= Frame( mainwindow, bg="#303b58", height= 184, width= 350, bd=0 )
Fileprev = Frame( mainwindow, bg="#404b69", height= 180, width= 346, bd=0 )
Imageprev = Label( Fileprev, bg="#404b69", justify='left')
Fileprev.place(x=14, y= 14)
Fileprevb.place(x=12, y= 12)
Imageprev.place(x=0, y=0)
Imageinput.place(x=8, y= 202)

class ButtonsCommands:
# Functions That Deals With Finding And Inheriting Values                       
  def ask_image_folder(): 
    with open(config_dir, 'r') as readconfig:
      tojson = load(readconfig)['Outputfolder_Path']
      the_imagefolder_path = filedialog.askopenfilename( initialdir = tojson, title = "Select Image File",
                             filetypes = (("Image Files","*.jpg *.png *.jpeg"),("Image Files","*.jpg *.png *.jpeg")))
      if the_imagefolder_path:
        image_details.clear()
        GetImageDetails(the_imagefolder_path).getimagename()
        for index in range(0, len(the_imagefolder_path), 1000):
          Imageinput.config(text="Image Folder : "+the_imagefolder_path[index:index+45]+"...")
          with Image.open(the_imagefolder_path).resize((368,218)) as intputimg:
            chosen_img = ImageTk.PhotoImage(intputimg)
            Imageprev.config(image=chosen_img, height= 210, width= 346)
          mainwindow.mainloop()

  def launch_create_sky():
    try:
      percentage = StringVar()
      progresswindow = Toplevel()
      progresswindow.geometry('380x90')
      progresswindow.title("Building Sky")
      progresswindow.resizable(False, False)
      progresswindow.iconbitmap('res\\title\\conversion.ico')
      progresswindow.config(background='#283149')
      createSKY.config(command=progresswindow.focus_set)
      create_process = Progressbar(progresswindow, length=338)
      Label(progresswindow, bg='#283149', textvariable=percentage, fg=f).place(x=380/2-15, y=50)
      create_process.place(x=20, y=20)
      processcubeimg = CreateCubeIMG(progresswindow, create_process, percentage)
      Thread(target=processcubeimg.getcreatesky).start()
      Thread(target=processcubeimg.loadingtitle).start()
      progresswindow.wait_window()
      createSKY.config(command=ButtonsCommands.launch_create_sky)
    except IndexError: processcubeimg.noimagehandler()
    except _tkinter.TclError: pass

  def goto_output_folder():
    with open(config_dir, 'r') as readconfig:
      readusingjson = load(readconfig)
      outpath = readusingjson['Outputfolder_Path']
      coroutoath = outpath.replace("/", "\\")
      showfolder(['explorer', coroutoath])

# mainwindow ( Oparating Buttons )
Button( mainwindow, text="OPEN", font=font_details[1], bg=ab, fg=f, activebackground=f, padx=x, pady=y, bd= yb,

        activeforeground=ab, relief='flat', command=ButtonsCommands.ask_image_folder ).place( x=10, y=yp )
Button( mainwindow, text="FOLDER", font=font_details[1], bg=ab, fg=f, activebackground = f, activeforeground=ab, 
        padx=x, pady=y, relief='flat', command = ButtonsCommands.goto_output_folder, bd= yb ).place( x=89, y=yp )
createSKY = Button( mainwindow, text="CREATE", font=font_details[1], bd=yb, fg=f, activebackground = f, padx = x,
                    pady = y, bg = ab, relief= 'flat', activeforeground=ab,  command=ButtonsCommands.launch_create_sky)
showSettings = Button( mainwindow, text="SETTINGS", font=font_details[1], bg=ab, fg=f, padx = x, pady = y,
                       activebackground= f, activeforeground=ab, relief= 'flat', bd= yb )
showSettings.config(command = SettingsWindow(showSettings).loadsettings)
createSKY.place( x=180.499, y=yp )
showSettings.place( x=270.499, y=yp )

# Window Loop Clossing
mainwindow.mainloop()
