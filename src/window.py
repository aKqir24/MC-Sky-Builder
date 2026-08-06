from config import *
import customtkinter as ctk
from customtkinter import StringVar
from tkinter import filedialog, TclError
from create import CreateCubeIMG, PackingPack
from worker import GetImageDetails
from settings import SettingsWindow, Thread, resetto, BooleanVar

class ButtonsCommands:
  #? Functions to be called by the button
  def ask_image_folder(self, Imageprev, Imageinput): 
    current_dir = configs['Output_Folder']
    the_imagefolder_path = filedialog.askopenfilename( initialdir = current_dir, title = "Select Image File",
                             filetypes = (("Image Files","*.jpg *.png *.jpeg"),("Image Files","*.jpg *.png *.jpeg")))
    if the_imagefolder_path:
      image_details.clear()
      GetImageDetails(the_imagefolder_path).getimagename()
      for index in range(0, len(the_imagefolder_path), 1000):
        Imageinput.configure(text="Image Folder : "+the_imagefolder_path[index:index+45]+"...")
        with Image.open(the_imagefolder_path).resize((368,218)) as intputimg:
          chosen_img = ImageTk.PhotoImage(intputimg)
          Imageprev.configure(image=chosen_img, height= 210, width= 350)

  def launch_create_sky(createSKY):
    pack_name = lambda: image_details.append(user_pack_name)

    def on_closing():
      running = False  
      PackingPack().clean_up()
      progresswindow.destroy()

    try:
      percentage = StringVar()
      progresswindow = ctk.CTkToplevel()
      progresswindow.geometry('380x90')
      progresswindow.minsize(380, 90)
      progresswindow.title("Building Sky")
      progresswindow.resizable(False, False)
      try:
          progresswindow.iconbitmap(f'{title_icon_path}conversion.ico')
      except Exception:
          pass
      progresswindow.configure(fg_color='#283149')
      createSKY.configure(command=progresswindow.focus_set)
      create_process = ctk.CTkProgressBar(progresswindow, width=338, fg_color="#303b58", progress_color=ab)
      create_process.set(0)
      ctk.CTkLabel(progresswindow, fg_color='transparent', textvariable=percentage, text_color=f, font=font_details[2]).place(x=380/2-15, y=50)
      create_process.place(x=20, y=20)
      progresswindow.protocol("WM_DELETE_WINDOW", on_closing)
      processcubeimg = CreateCubeIMG(progresswindow, create_process, percentage)
      Thread(target=processcubeimg.getcreatesky).start()
      Thread(target=processcubeimg.loadingtitle).start()
      progresswindow.wait_window()
      createSKY.configure(command=lambda: ButtonsCommands.launch_create_sky(createSKY))
    except IndexError: processcubeimg.noimagehandler()
    except (TclError, Exception): pass

  def goto_output_folder():
    import platform
    import subprocess
    import os
    outpath = str(configs['Output_Folder'])
    system = platform.system()
    try:
      if system == "Windows":
        os.startfile(outpath)
      elif system == "Darwin":
        subprocess.Popen(['open', outpath])
      else:
        subprocess.Popen(['xdg-open', outpath])
    except Exception as e:
      print(f"Could not open folder: {e}")

class MainWindow(ctk.CTk): 
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.geometry('376x268')
        self.title("MC Sky Builder")
        self.configure(fg_color="#283149")
        try:
            self.iconbitmap(f'{title_icon_path}app.ico')
        except Exception:
            pass
        self.resizable(False, False)

        # Labels/Frames of the path & location with modern CustomTkinter card styling
        Imageinput = ctk.CTkLabel( self, text="Image Folder :", fg_color="transparent", text_color=f, font=font_details[1] )
        Fileprev = ctk.CTkFrame( self, fg_color="#404b69", height= 180, width= 350, corner_radius=8, border_width=1, border_color="#303b58" )
        Imageprev = ctk.CTkLabel( Fileprev, fg_color="transparent", text="", justify='left')
        Fileprev.place(x=13, y= 13)
        Imageprev.place(x=0, y=0)
        Imageinput.place(x=10, y= 202)  
    
        # Place the main buttons with even spacing and sleek modern styling
        btn_font = font_details[2]
        btn_width = 78
        ctk.CTkButton( self, text="OPEN", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=btn_width, height=28,
                       command=lambda: ButtonsCommands.ask_image_folder(self, Imageprev, Imageinput) ).place( x=12, y=yp )
        ctk.CTkButton( self, text="FOLDER", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=btn_width, height=28,
                       command = ButtonsCommands.goto_output_folder ).place( x=102, y=yp )
        createSKY = ctk.CTkButton( self, text="CREATE", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=btn_width, height=28,
                                   command=lambda: ButtonsCommands.launch_create_sky(createSKY))
        showSettings = ctk.CTkButton( self, text="SETTINGS", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=btn_width, height=28 )
        showSettings.configure(command = lambda: SettingsWindow(showSettings))
        createSKY.place( x=192, y=yp )
        showSettings.place( x=282, y=yp )
           
        self.mainloop()


