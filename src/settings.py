import about
from config import *
from threading import Thread
import customtkinter as ctk
from customtkinter import BooleanVar, StringVar
from tkinter import filedialog
from worker import EnvironmentInitializer as resetto, ConfigurationManager as ConfigManagement
from os import remove as rm, path

class SkySettingsWindow(ctk.CTkToplevel):
  def __init__ (self, settingsbutton):
    super().__init__()
    self.settings_button = settingsbutton
    self.pack_to_zip_var = BooleanVar()
    self.pack_to_mcpack_var = BooleanVar()

    self.focus_set()
    self.title("Settings")
    self.geometry('460x220')
    self.configure(fg_color=db)
    self.resizable(False, False)
    try:
        self.iconbitmap(f'{title_icon_path}manufacturing.ico')
    except Exception:
        pass
    self.settings_button.configure(command=self.focus_set)

    # Checkboxes for packing options with built-in text
    label_font = font_details[1]
    packing_mcpack_ch = ctk.CTkCheckBox( self, text="Convert Into .mcpack", variable=self.pack_to_mcpack_var, fg_color=ab, hover_color="#006b73", font=label_font, text_color=f, width=18, height=18, corner_radius=4 )
    packing_zip_ch = ctk.CTkCheckBox( self, text="Convert Into .zip", variable=self.pack_to_zip_var, fg_color=ab, hover_color="#006b73", font=label_font, text_color=f, width=18, height=18, corner_radius=4 )

    packing_mcpack_ch.place(x=250, y=75)
    packing_zip_ch.place(x=250, y=105)

    the_zippacker = configs['Convert_To_Zip']
    the_mcpacker = configs['Convert_To_Mcpack']
    if the_zippacker == False: packing_zip_ch.deselect()
    else: packing_zip_ch.select()
    if the_mcpacker == False: packing_mcpack_ch.deselect()
    else: packing_mcpack_ch.select()

    # Modern card background for output path
    output_path_bg = ctk.CTkFrame(self, fg_color=b, height=28, width=360, corner_radius=6 )
    output_folder_label = ctk.CTkLabel(self, fg_color=b, text_color=f, text="", font=font_details[1] )
    ctk.CTkLabel(self, text="Output Folder", fg_color=db, text_color=f, font=font_details[2]).place(x=16, y=8)
    ctk.CTkLabel(self, text="Sky Resolution", fg_color=db, text_color=f, font=font_details[2]).place(x=16, y=55)
    output_path_bg.place(x=84, y= 32)
    output_folder_label.place(x=90, y= 32)

    the_outputfolder_path = configs['Output_Folder']
    if the_outputfolder_path:
      for index in range(0, len(the_outputfolder_path), 1000):
         output_folder_label.configure(text=the_outputfolder_path[index:index+55]+"...")

    picked_options = [ output_resolution, packing_zip_ch, packing_mcpack_ch, output_folder_label ]
    option_variables = [ self.pack_to_zip_var, self.pack_to_mcpack_var ]
    settingbuttons = SettingsActionHandler(picked_options, self, option_variables)

    # Clean modern buttons with uniform aesthetic and even spacing
    btn_font = font_details[2]
    btn_w = 96
    btn_y = 175
    ctk.CTkButton(self, command=settingbuttons.ask_output_folder, text="CHANGE",
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=64, height=26).place(x=16, y=32)
    ctk.CTkButton(self, command=settingbuttons.aboutprogram, text="ABOUT",
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=30).place(x=16, y=btn_y)
    ctk.CTkButton(self, command=settingbuttons.resetsettings, text="RESET",
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=30).place(x=124, y=btn_y)
    apply = ctk.CTkButton( self, command=settingbuttons.applysettings, text="APPLY",
            font=btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=30 )
    apply.place(x=232, y=btn_y)
    ctk.CTkButton(self, command=settingbuttons.closesettings, text="CLOSE",
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=30).place(x=340, y=btn_y)

    self.wait_window()
    self.settings_button.configure(command = lambda: SkySettingsWindow(self.settings_button))


class SettingsActionHandler:
    def __init__ (self, options, settingswindow, option_variables):
      self.options=options
      self.settingswindow=settingswindow
      self.settingsconfigs = ConfigurationManager(options[0], option_variables[0], option_variables[1])

    closesettings = lambda self:self.settingswindow.destroy()
    aboutprogram = lambda self:about.AboutWindow().show()

    def ask_output_folder(self):
      userdesktop = default_output_path
      the_outputfolder_path = filedialog.askdirectory( initialdir=userdesktop, title="Select Output Folder" )
      if the_outputfolder_path:
        self.settingsconfigs.userpath(the_outputfolder_path)
        self.settingswindow.focus_set()
        for index in range(0, len(the_outputfolder_path), 1000):
          self.options[3].configure(text=the_outputfolder_path[index:index+45]+"...")

    def resetsettings(self):
        rm(config_file)
        resetto().setdefaults()
        self.options[0].set(0)
        self.options[1].deselect()
        self.options[2].deselect()
        the_outputfolder_path = readconfig()[1]
        for index in range(0, len(the_outputfolder_path), 1000):
          self.options[3].configure(text=the_outputfolder_path[index:index+49]+"...")

    def applysettings(self):
      settingswindow=self
      def savelabel():
        setsvlb = ctk.CTkLabel(self.settingswindow, fg_color=db, text_color=f, text="Saved!!", font=font_details[2])
        setsvlb.place(x=271, y=125), sleep(2)
        setsvlb.destroy()

      Thread(target=self.settingsconfigs.write_settings_config).start()
      Thread(target=savelabel).start()
      self.settingswindow.focus_set()
