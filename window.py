# Program Information
__author__: "Akqir"
__version__: "1.1.0"
__program_name__: "MC-Sky-Builder"
__description__: "Converts an Image into a sky-overlay pack for minecraft..."

class ButtonsCommands:
  #? Functions to be called by the button
  def ask_image_folder(mainwindow, Imageprev, Imageinput): 
    with open(config_dir, 'r') as readconfig:
      tojson = load(readconfig)['Outputfolder_Path']
      the_imagefolder_path = filedialog.askopenfilename( initialdir = tojson, title = "Select Image File",
                             filetypes = (("Image Files","*.jpg *.png *.jpeg"),("Image Files","*.jpg *.png *.jpeg")))
      if the_imagefolder_path:
        image_details.clear()
        # TODO: Make an If statement when a user_pack name is present
        # TODO: And if not then use the default image name as pack name
        GetImageDetails(the_imagefolder_path).getimagename()
        for index in range(0, len(the_imagefolder_path), 1000):
          Imageinput.config(text="Image Folder : "+the_imagefolder_path[index:index+45]+"...")
          with Image.open(the_imagefolder_path).resize((368,218)) as intputimg:
            chosen_img = ImageTk.PhotoImage(intputimg)
            Imageprev.config(image=chosen_img, height= 210, width= 350)
          mainwindow.mainloop()

  def launch_create_sky(createSKY):
    from tkinter.ttk import Progressbar
    def on_closing():
      running = False  #? Stop the loop
      PackingPack().CleanUp()
      progresswindow.destroy() #? Close the top-level window

    # TODO: Make a dialog that ask for your own pack name!!
    def pack_name(): image_details.append(user_pack_name)

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
      progresswindow.protocol("WM_DELETE_WINDOW", on_closing)
      processcubeimg = CreateCubeIMG(progresswindow, create_process, percentage)
      Thread(target=processcubeimg.getcreatesky).start()
      Thread(target=processcubeimg.loadingtitle).start()
      progresswindow.wait_window()
      createSKY.config(command=lambda: ButtonsCommands.launch_create_sky(createSKY))
    except IndexError: processcubeimg.noimagehandler()
    except _tkinter.TclError: pass

  def goto_output_folder():
    from subprocess import Popen as showfolder
    with open(config_dir, 'r') as readconfig:
      readusingjson = load(readconfig)
      outpath = readusingjson['Outputfolder_Path']
      coroutoath = outpath.replace("/", "\\")
      showfolder(['explorer', coroutoath])

class MainWindow(): 
  def WindowInterface():
    #* Main window of the program
    mainwindow = Tk()
    mainwindow.geometry('376x268')
    mainwindow.title("MC Sky Builder")
    mainwindow.config(background="#283149")
    mainwindow.iconbitmap('res\\icon.ico')
    mainwindow.resizable(False, False)

    # Labels/Frames of the path & location
    Imageinput = Label( mainwindow, text="Image Folder :", bg="#283149", fg=f, pady= 1, bd=0 )
    Fileprevb= Frame( mainwindow, bg="#303b58", height= 184, width= 354, bd=0 )
    Fileprev = Frame( mainwindow, bg="#404b69", height= 180, width= 350, bd=0 )
    Imageprev = Label( Fileprev, bg="#404b69", justify='left')
    Fileprev.place(x=14, y= 14), Fileprevb.place(x=12, y= 12)
    Imageprev.place(x=0, y=0), Imageinput.place(x=8, y= 202)  
    
    def FrontButtons():
      # Place the main buttons
      Button( mainwindow, text="OPEN", font=font_details[1], bg=ab, fg=f, activebackground=f, padx=x, pady=y, bd= yb, activeforeground=ab, 
              relief=rel, command=lambda: ButtonsCommands.ask_image_folder(mainwindow, Imageprev, Imageinput) ).place( x=10, y=yp )
      Button( mainwindow, text="FOLDER", font=font_details[1], bg=ab, fg=f, activebackground = f, activeforeground=ab, 
              padx=x, pady=y, relief=rel, command = ButtonsCommands.goto_output_folder, bd= yb ).place( x=89, y=yp )
      createSKY = Button( mainwindow, text="CREATE", font=font_details[1], bd=yb, fg=f, activebackground = f, padx = x, pady = y, 
                          bg = ab, relief= rel, activeforeground=ab,  command=lambda: ButtonsCommands.launch_create_sky(createSKY))
      showSettings = Button( mainwindow, text="SETTINGS", font=font_details[1], bg=ab, fg=f, padx = x, pady = y,
                              activebackground= f, activeforeground=ab, relief= rel, bd= yb )
      showSettings.config(command = SettingsWindow(showSettings).loadsettings)
      createSKY.place( x=180.499, y=yp )
      showSettings.place( x=270.499, y=yp )
      
    # Call Window Loop Clossing
    return FrontButtons(), mainwindow.mainloop() 

if __name__ == '__main__':
  #* At First I will GOD is Good All The Time :) *#
  from all_val import *
  from tkinter import Tk, Button, _tkinter
  from create import CreateCubeIMG, PackingPack
  from worker import GetImageDetails, filedialog, Toplevel, Label, StringVar
  from settings import SettingsWindow, Frame, BooleanVar, Thread, resetto
  resetto().makethetempdir().setdefaults(), MainWindow.WindowInterface()