#* At First I will GOD is Good All The Time :) *#
from config import *
from tkinter import Tk, Button, _tkinter
from create import CreateCubeIMG, PackingPack
from worker import GetImageDetails, filedialog, Toplevel, Label, StringVar
from settings import SettingsWindow, Frame, BooleanVar, Thread, resetto

class ButtonsCommands:
  #? Functions to be called by the button
  def ask_image_folder(self, Imageprev, Imageinput): 
    current_dir = configs['Output_Folder']
    the_imagefolder_path = filedialog.askopenfilename( initialdir = current_dir, title = "Select Image File",
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

  def launch_create_sky(createSKY):
    from tkinter.ttk import Progressbar
    # TODO: Make a dialog that ask for your own pack name...
    pack_name = lambda: image_details.append(user_pack_name)

    def on_closing():
      running = False  #? Stop the loop
      PackingPack().CleanUp()
      progresswindow.destroy() #? Close the top-level window 

    try:
      percentage = StringVar()
      progresswindow = Toplevel()
      progresswindow.geometry('380x90')
      progresswindow.title("Building Sky")
      progresswindow.resizable(False, False)
      progresswindow.iconbitmap(f'{title_icon_path}conversion.ico')
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
    outpath = str(configs['Output_Folder'].replace("/", "\\"))
    showfolder(['explorer', outpath])

class MainWindow(Tk): 
    #* Main window of the program
    def __init__(self):
        super().__init__()
        self.geometry('376x268')
        self.title("MC Sky Builder")
        self.config(background="#283149")
        self.iconbitmap(f'{title_icon_path}app.ico')
        self.resizable(False, False)

        # Labels/Frames of the path & location
        Imageinput = Label( self, text="Image Folder :", bg="#283149", fg=f, pady= 1, bd=0 )
        Fileprevb= Frame( self, bg="#303b58", height= 184, width= 354, bd=0 )
        Fileprev = Frame( self, bg="#404b69", height= 180, width= 350, bd=0 )
        Imageprev = Label( Fileprev, bg="#404b69", justify='left')
        Fileprev.place(x=14, y= 14), Fileprevb.place(x=12, y= 12)
        Imageprev.place(x=0, y=0), Imageinput.place(x=8, y= 202)  
    
        # Place the main buttons
        Button( self, text="OPEN", font=font_details[1], bg=ab, fg=f, activebackground=f, padx=x, pady=y, bd= yb, activeforeground=ab, 
                  relief=rel, command=lambda: ButtonsCommands.ask_image_folder(self, Imageprev, Imageinput) ).place( x=10, y=yp )
        Button( self, text="FOLDER", font=font_details[1], bg=ab, fg=f, activebackground = f, activeforeground=ab, 
                  padx=x, pady=y, relief=rel, command = ButtonsCommands.goto_output_folder, bd= yb ).place( x=89, y=yp )
        createSKY = Button( self, text="CREATE", font=font_details[1], bd=yb, fg=f, activebackground = f, padx = x, pady = y, 
                              bg = ab, relief= rel, activeforeground=ab,  command=lambda: ButtonsCommands.launch_create_sky(createSKY))
        showSettings = Button( self, text="SETTINGS", font=font_details[1], bg=ab, fg=f, padx = x, pady = y,
                                  activebackground= f, activeforeground=ab, relief= rel, bd= yb )
        showSettings.config(command = lambda: SettingsWindow(showSettings))
        createSKY.place( x=180.499, y=yp )
        showSettings.place( x=270.499, y=yp )
           
        # Call Window Loop Clossing
        self.mainloop()

if __name__ == '__main__':
    resetto().makethetempdir().setdefaults(), MainWindow()
