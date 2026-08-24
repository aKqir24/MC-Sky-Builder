from . import about
from .config import *
from .worker import EnvironmentInitializer as resetto, ConfigurationManager

from CTkToolTip import *
from tkinter import filedialog
from PIL import Image
from time import sleep
from threading import Thread
import customtkinter as ctk
from customtkinter import BooleanVar
from os import remove as rm, path

class SkySettingsWindow(ctk.CTkToplevel):
  def __init__ (self, settingsbutton):
    super().__init__()
    self.settings_button = settingsbutton

    self.focus_set()
    self.title("Settings")
    self.geometry('378x208')
    self.minsize(428, 200)
    self.resizable(False, False)
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.settings_button.configure(command=self.focus_set)
    self.widgets()
    try: self.iconbitmap(f'{title_icon_path}manufacturing.ico')
    except Exception: pass

  def widgets(self):
    # Main window containers
    label_font = font_details[1]
    switch_wrapper = ctk.CTkFrame(self, height= 420, width= 342, fg_color="transparent")
    switch_wrapper.grid(row=2, column=0,padx=16, pady=14, columnspan=4, sticky="wn")
    widget_buttons_wrapper_left = ctk.CTkFrame(self, height=295, width=240, fg_color="transparent")
    widget_buttons_wrapper_left.grid(row=3, column=0,padx=16, pady=(0, 14), sticky="wn")
    widget_buttons_wrapper_right = ctk.CTkFrame(self, height=295, width=240, fg_color="transparent")
    widget_buttons_wrapper_right.grid(row=3, column=1, padx=16, pady=(0, 14), sticky="en")

    # Switch for packing options with built-in text
    packing_mcpack_toggle = ctk.CTkSwitch(switch_wrapper, onvalue=True, offvalue=False, text="Mcpack Output", font=label_font, corner_radius=8)
    packing_zip_toggle = ctk.CTkSwitch(switch_wrapper, onvalue=True, offvalue=False, text="Zip Output", font=label_font, corner_radius=8)
    packing_mcpack_toggle.grid(row=0, column=0, pady=2, padx=8, sticky="we")
    packing_zip_toggle.grid(row=1, column=0, pady=2, padx=8, sticky="wn")

    auto_save_toggle = ctk.CTkSwitch(switch_wrapper, onvalue=True, offvalue=False, text="Auto save", font=label_font, corner_radius=8)
    ask_packname_toggle = ctk.CTkSwitch(switch_wrapper, onvalue=True, offvalue=False, text="Ask packname", font=label_font, corner_radius=8)
    auto_save_toggle.grid(row=0, column=1, pady=2, ipadx=8, padx=8, sticky="wn")
    ask_packname_toggle.grid(row=1, column=1, pady=2, padx=8, sticky="wn")

    # Setting Tooltips
    self.auto_save_tooltip = CTkToolTip(auto_save_toggle, delay=0.5, message="Will always save both settings and current sky slider values", always_on_top=True)

    # Modern card background for output path
    output_folder_label = ctk.CTkLabel(self, border_width=2, border_color="#709775", height=34, font=font_details[1], corner_radius=8, anchor="w")
    ctk.CTkLabel(self, text="Output Folder:", font=font_details[2]).grid(row=0, column=0, ipadx=1, padx=6, pady=(16, 8), sticky="wn")
    output_folder_label.grid(row=1, column=0, ipadx=8, padx=(16, 2), sticky="ews")

    change_path_label(output_folder_label)
    widgets = [ packing_zip_toggle, packing_mcpack_toggle, auto_save_toggle, ask_packname_toggle ]
    settingbuttons = SettingsActionHandler(widgets, self, output_folder_label)

    # Clean modern buttons with uniform aesthetic and even spacing
    btn_font = font_details[2]
    self.about_icon = ctk.CTkImage(dark_image=Image.open(str(RESOURCE_DIR / "actions" / "about.png")), size=(28, 28))
    self.close_icon = ctk.CTkImage(dark_image=Image.open(str(RESOURCE_DIR / "actions" / "close.png")), size=(28, 28))
    self.apply_icon = ctk.CTkImage(dark_image=Image.open(str(RESOURCE_DIR / "actions" / "apply.png")), size=(28, 28))
    ctk.CTkButton(self, command=settingbuttons.ask_output_folder, text="CHANGE", font=btn_font, corner_radius=6, width=1, height=32
                 ).grid(row=1, column=1, ipadx=8, ipady=1, padx=(8, 16), columnspan=1, sticky="we")
    ctk.CTkButton(widget_buttons_wrapper_left, command=settingbuttons.aboutprogram, image=self.about_icon, text="",
           font=btn_font, corner_radius=6, width=28, height=30).grid(row=0, column=0, ipadx=0)
    ctk.CTkButton(widget_buttons_wrapper_left, command=settingbuttons.resetsettings, text="RESET",
           font=btn_font, corner_radius=6, width=88, height=30).grid(row=0, column=1, ipadx=4, ipady=2, padx=4)
    apply = ctk.CTkButton(widget_buttons_wrapper_right, command=settingbuttons.applysettings, text="", image=self.apply_icon,
            font=btn_font, corner_radius=6, width=28, height=30)
    apply.grid(row=0, column=0, ipadx=4, padx=4)
    ctk.CTkButton(widget_buttons_wrapper_right, command=settingbuttons.closesettings, text="", image=self.close_icon,
           font=btn_font, corner_radius=6, width=28, height=30).grid(row=0, column=1, ipadx=4)

    self.wait_window()
    self.settings_button.configure(command = lambda: SkySettingsWindow(self.settings_button))

class SettingsActionHandler:
    def __init__ (self, widgets, settings_window, output_folder_label):
      self.widgets=widgets
      self.output_folder_label = output_folder_label
      self.settings_window=settings_window
      self.settingsconfigs = ConfigurationManager(widgets)

    closesettings = lambda self:self.settings_window.destroy()
    aboutprogram = lambda self:about.AboutWindow()

    def ask_output_folder(self):
        the_outputfolder_path = filedialog.askdirectory(initialdir=default_output_path, title="Select Output Folder")
        if the_outputfolder_path:
          self.settingsconfigs.stored_config['settings']['output_folder']
          self.settings_window.focus_set()
          change_path_label(self.output_folder_label, the_outputfolder_path, 45)

    def resetsettings(self):
        if path.exists(config_file): rm(config_file)
        resetto().setdefaults()
        self.settingsconfigs.update_switch(True)
        change_path_label(self.widgets[2], readconfig()['settings']['output_folder'], 49)

    def applysettings(self):
      def savelabel():
        setsvlb = ctk.CTkLabel(self.settings_window, text="Saved!!", font=font_details[2])
        setsvlb.place(x=271, y=125), sleep(2)
        setsvlb.destroy()

      Thread(target=self.settingsconfigs.write_settings_config).start()
      Thread(target=savelabel).start()
      self.settingsconfigs.update_switch()
      self.settings_window.focus_set()
