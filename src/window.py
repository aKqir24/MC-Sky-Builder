from config import *
import customtkinter as ctk
from customtkinter import StringVar
from tkinter import filedialog, TclError
from create import CubeMapImageProcessor, ResourcePackBuilder
from worker import GetImageDetails
from settings import SkySettingsWindow, Thread, resetto, BooleanVar

class SkyBuilderActions:
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
        with Image.open(the_imagefolder_path).resize((412,195)) as intputimg:
          chosen_img = ImageTk.PhotoImage(intputimg)
          Imageprev.configure(image=chosen_img, height= 195, width= 412)

  def launch_create_sky(createSKY):
    pack_name = lambda: image_details.append(user_pack_name)

    def on_closing():
      running = False
      ResourcePackBuilder().clean_up()
      progresswindow.destroy()

    try:
      percentage = StringVar()
      progresswindow = ctk.CTkToplevel()
      progresswindow.geometry('420x110')
      progresswindow.minsize(420, 110)
      progresswindow.title("Building Sky")
      progresswindow.resizable(False, False)
      try:
          progresswindow.iconbitmap(f'{title_icon_path}conversion.ico')
      except Exception:
          pass
      progresswindow.configure(fg_color='#283149')
      createSKY.configure(command=progresswindow.focus_set)
      create_process = ctk.CTkProgressBar(progresswindow, width=380, height=14, fg_color="#303b58", progress_color=ab)
      create_process.set(0)
      ctk.CTkLabel(progresswindow, fg_color='transparent', textvariable=percentage, text_color=f, font=font_details[2]).place(x=420/2-20, y=65)
      create_process.place(x=20, y=25)
      progresswindow.protocol("WM_DELETE_WINDOW", on_closing)
      processcubeimg = CubeMapImageProcessor(progresswindow, create_process, percentage)
      Thread(target=processcubeimg.getcreatesky).start()
      Thread(target=processcubeimg.loadingtitle).start()
      progresswindow.wait_window()
      createSKY.configure(command=lambda: SkyBuilderActions.launch_create_sky(createSKY))
    except IndexError: processcubeimg.noimagehandler()
    except (TclError, Exception): pass

  def goto_output_folder():
    import platform
    import subprocess
    outpath = str(configs['Output_Folder'])
    system = platform.system()
    try:
      if system == "Windows":
        from os import startfile
        startfile(outpath)
      elif system == "Darwin":
        subprocess.Popen(['open', outpath])
      else:
        subprocess.Popen(['xdg-open', outpath])
    except Exception as e:
      print(f"Could not open folder: {e}")



class SkyBuilderWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.geometry('628x318')
        self.title("MC Sky Builder")
        self.configure(fg_color="#283149")
        try:
            self.iconbitmap(f'{title_icon_path}app.ico')
        except Exception:
            pass
        self.resizable(False, False)

        # Widget Containers
        primary_container = ctk.CTkFrame( self, height= 295, width= 342, fg_color="transparent")
        primary_container.pack(side="left", padx=6, pady=6, fill="both", expand=True)

        # Labels/Frames of the path & location with modern CustomTkinter card styling
        input_wrapper = ctk.CTkFrame( primary_container, fg_color="transparent", corner_radius=8 )
        main_buttons_container=ctk.CTkFrame( input_wrapper, fg_color="transparent", corner_radius=8 )
        main_slider_container=ctk.CTkFrame( primary_container, fg_color="transparent", corner_radius=8 )
        image_input = ctk.CTkLabel( input_wrapper, text="", corner_radius=8, height=34, width= 248, fg_color=b, text_color=f, font=font_details[1] )
        image_preview = ctk.CTkLabel(primary_container, corner_radius=8, height= 195, width= 336, fg_color=b2, text="")
        image_preview.grid(row=0, column=0, padx=12, pady=12)
        input_wrapper.grid(row=1, column=0, sticky="n")
        main_slider_container.grid(row=0, column=6, rowspan=6, padx=4)
        main_buttons_container.grid(row=1, column=0, columnspan=4, pady=8)
        image_input.grid(row=0, column=0, ipadx=4, padx=4)

        # Place the main buttons with even spacing and sleek modern styling
        btn_font = font_details[2]
        ctk.CTkButton( input_wrapper, text="OPEN", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=58, height=32,
                       command=lambda: SkyBuilderActions.ask_image_folder(self, Imageprev, Imageinput) ).grid(row=0, column=1, ipadx=6, padx=4)
        ctk.CTkButton( main_buttons_container, text="FOLDER", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=68, height=32,
                       command = SkyBuilderActions.goto_output_folder ).grid(row=1, column=1, ipadx=18, padx=4)
        createSKY = ctk.CTkButton( main_buttons_container, text="CREATE", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=68, height=32,
                                   command=lambda: SkyBuilderActions.launch_create_sky(createSKY))
        showSettings = ctk.CTkButton( main_buttons_container, text="SETTINGS", font=btn_font, fg_color=ab, text_color=f, hover_color="#006b73", corner_radius=6, width=68, height=32 )
        showSettings.configure(command = lambda: SkySettingsWindow(showSettings))
        createSKY.grid(row=1, column=2, ipadx=18, padx=4)
        showSettings.grid(row=1, column=3, ipadx=18, padx=4)

        ctk.CTkLabel( main_slider_container, text="Resolution:").grid(row=0, column=1, sticky="wn")
        output_resolution = ctk.CTkSlider( main_slider_container, to=3, from_=0, width=240, fg_color=b, progress_color=ab, button_color=ab, button_hover_color="#006b73", number_of_steps=3, height=16 )
        output_resolution.grid(row=1, column=1, padx=2)

        ctk.CTkLabel( main_slider_container, text="Curvature:").grid(row=2, column=1, sticky="wn")
        output_curvature = ctk.CTkSlider( main_slider_container, to=400, from_=200, width=240, fg_color=b, progress_color=ab, button_color=ab, button_hover_color="#006b73", height=16 )
        output_curvature.grid(row=3, column=1, padx=2)

        ctk.CTkLabel( main_slider_container, text="Edge Blend:").grid(row=4, column=1, sticky="wn")
        output_edge_blend = ctk.CTkSlider( main_slider_container, to=100, from_=50, width=240, fg_color=b, progress_color=ab, button_color=ab, button_hover_color="#006b73", height=16 )
        output_edge_blend.grid(row=5, column=1, padx=2)

        custom_resolution_wrapper = ctk.CTkFrame( main_slider_container, fg_color="transparent", corner_radius=8 )
        custom_resolution_wrapper.grid(row=7, column=1, pady=16, padx=2, sticky="wn")
        custom_resolution_val = ctk.CTkEntry(custom_resolution_wrapper, placeholder_text="Custom Resolution", font=font_details[1], fg_color=b, border_color=b2, placeholder_text_color="#626f91", width=200, corner_radius=8 )
        custom_resolution_val.grid(row=0, column=1, padx=2, ipady=2)

        custom_resolution_toggle = ctk.StringVar(value="off")
        enable_custom_resolution = ctk.CTkCheckBox(custom_resolution_wrapper, text="", fg_color=ab, hover_color="#006b73", font=font_details[1], text_color=f,
                                     width=18, height=18, corner_radius=6, border_width=3, border_color=b,
                                     variable=custom_resolution_toggle, onvalue="on", offvalue="off")
        enable_custom_resolution.grid(row=0, column=2, padx=6, ipady=2)

        self.mainloop()
