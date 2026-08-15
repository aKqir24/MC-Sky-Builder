import customtkinter as ctk
from customtkinter import StringVar, CTkImage
from tkinter import TclError, filedialog
from PIL import Image, ImageDraw

from .config import *
from .worker import GetImageDetails
from .create import CubeMapImageProcessor, ResourcePackBuilder
from .settings import SkySettingsWindow, Thread, resetto, BooleanVar

class SkyBuilderActions:
  #? Functions to be called by the button
  go_output_folder = lambda: open_folder(configs['settings']['output_folder'])

  def ask_image_folder(self, img_input, img_prev):
    current_dir = configs['settings']['output_folder']
    the_imagefolder_path = filedialog.askopenfilename(initialdir=current_dir, title="Select Image File", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if the_imagefolder_path:
      image_details.clear()
      GetImageDetails(the_imagefolder_path).get_image_name()
      change_path_label(img_input, the_imagefolder_path, 32)
      with Image.open(the_imagefolder_path) as input_img:
        rgba_img = input_img.convert("RGBA")
        mask = Image.new("L", rgba_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), rgba_img.size], radius=82, fill=255)
        rgba_img.putalpha(mask)
        img_prev.configure(image=CTkImage(dark_image=rgba_img, light_image=rgba_img, size=(326, 166)), height= 165, width= 412)

  def launch_create_sky(create_btn):
    pack_name = lambda: image_details.append(user_pack_name)

    def on_closing():
      running = False
      ResourcePackBuilder().clean_up()
      progresswindow.destroy()

    try:
      percentage = StringVar()
      progresswindow = ctk.CTkToplevel()
      progresswindow.geometry('420x110')
      progresswindow.minsize(424, 110)
      progresswindow.title("Building Sky")
      progresswindow.resizable(False, False)
      try:
          progresswindow.iconbitmap(f'{title_icon_path}conversion.ico')
      except Exception:
          pass
      create_btn.configure(command=progresswindow.focus_set)
      create_process = ctk.CTkProgressBar(progresswindow, width=380, height=14)
      create_process.set(0)
      ctk.CTkLabel(progresswindow, textvariable=percentage, font=font_details[2]).place(x=420/2-20, y=65)
      create_process.place(x=20, y=25)
      progresswindow.protocol("WM_DELETE_WINDOW", on_closing)
      processcubeimg = CubeMapImageProcessor(progresswindow, create_process, percentage)
      Thread(target=processcubeimg.get_create_sky).start()
      Thread(target=processcubeimg.loading_title).start()
      progresswindow.wait_window()
      create_btn.configure(command=lambda: SkyBuilderActions.launch_create_sky(create_btn))
    except IndexError: processcubeimg.no_image_handler()
    except (TclError, Exception): pass

class SkyBuilderWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.geometry('682x298')
        self.minsize(682, 298)
        self.title("MC Sky Builder")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        try: self.iconbitmap(f'{title_icon_path}app.ico')
        except Exception: pass
        self.resizable(False, False)

        main_slider_container = ctk.CTkFrame(self)
        image_input = ctk.CTkLabel(self, border_width=2, border_color="#709775", text="Image path will go here...", height=32, padx=6, pady=0, anchor="w", font=font_details[1])
        image_preview = ctk.CTkLabel(self, border_width=1, border_color="#2b3a2c", fg_color="#18271a", text="", padx=0, pady=0, compound="center", height=195, width=336)
        image_preview.grid(row=0, column=0, ipadx=0, padx=14, pady=(14, 12), columnspan=3, sticky="wnse")
        main_slider_container.grid(row=0, column=6, padx=4, sticky="ew")
        image_input.grid(row=1, column=0, ipadx=6, padx=(16, 0), pady=(0, 4), columnspan=2, sticky="we")
        main_slider_container.grid(row=0, column=6, ipadx=8, ipady=8, rowspan=3, padx=(0, 16), pady=(14, 16), sticky="ewn")

        btn_font = font_details[2]
        ctk.CTkButton(self, text="OPEN", font=btn_font, height=32, command=lambda: SkyBuilderActions.ask_image_folder(self, image_input, image_preview) ).grid(row=1, column=2, ipadx=6, padx=(6, 16), sticky="nwe")
        ctk.CTkButton(self, text="FOLDER", font=btn_font, height=32, command=SkyBuilderActions.go_output_folder).grid(row=2, column=0, ipadx=18, padx=(16, 2), pady=(4, 16), sticky="nwe")
        create_btn = ctk.CTkButton(self, text="CREATE", font=btn_font, height=32, command=lambda: SkyBuilderActions.launch_create_sky(create_btn))
        settings_btn = ctk.CTkButton(self, text="SETTINGS", font=btn_font, height=32, command=lambda: SkySettingsWindow(settings_btn))
        create_btn.grid(row=2, column=1, ipadx=18, padx=2, pady=(4, 16), sticky="nwe")
        settings_btn.grid(row=2, column=2, ipadx=18, padx=(2, 16), pady=(4, 16), sticky="nwe")

        sliders_values = []
        entries_values = []

        sliders_config = [
            ("Resolution:", 0, 1, 3, 0, "e", 3),
            ("Curvature:", 2, 3, 3, 0.1, "e", None),
            ("Edge Blend:", 4, 5, 100, 50, "e", None),
            ("Saturation:", 6, 7, 100, 50, "e", None),
        ]

        for index, (text, lbl_row, frm_row, to_val, from_val, entry_sticky, steps) in enumerate(sliders_config):
            ctk.CTkLabel(main_slider_container, text=text, font=font_details[1]).grid(row=lbl_row, column=0, sticky="wn", pady=(8, 0), padx=(8, 0))

            section = ctk.CTkFrame(main_slider_container, fg_color="transparent")
            section.grid(row=frm_row, column=0, padx=(16, 0))

            entry = ctk.CTkEntry(section, width=54, height=26, font=font_details[1])
            entry.grid(row=1, column=0, padx=0, sticky=entry_sticky)
            entries_values.append(entry)

            def make_command(e=entry, i=index, s_steps=steps):
                return lambda val: (
                    e.delete(0, "end"),
                    e.insert(0, str(default_resolutions[int(val)] if i == 0 else (int(val) if s_steps else round(val, 1))))
                )

            slider_kwargs = dict(
                master=section, to=to_val, from_=from_val, width=188, height=16,
                command=make_command()
            )
            if steps: slider_kwargs["number_of_steps"] = steps

            slider = ctk.CTkSlider(**slider_kwargs)
            slider.grid(row=1, column=1, padx=6, sticky="e")
            sliders_values.append(slider)

            initial_val = int(slider.get())
            display_val = default_resolutions[initial_val] if index == 0 else initial_val
            entry.insert(0, str(display_val))
        self.mainloop()
