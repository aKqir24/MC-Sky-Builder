import about
from config import *
from threading import Thread
import customtkinter as ctk
from customtkinter import BooleanVar, StringVar
from tkinter import filedialog
from worker import ToDoDuringStartup as resetto, ConfigManagement, rm, path, load

class SettingsWindow(ctk.CTkToplevel):  
  def __init__ (self, settingsbutton):
    super().__init__()
    self.settings_button = settingsbutton
    self.pack_to_zip_var = BooleanVar()
    self.pack_to_mcpack_var = BooleanVar()

    self.focus_set()
    self.title("Settings")
    self.geometry('393x181')
    self.configure(fg_color=db)
    self.resizable(False, False)
    try:
        self.iconbitmap(f'{title_icon_path}manufacturing.ico')
    except Exception:
        pass
    self.settings_button.configure(command=self.focus_set)
    
    # Resolution slider with modern CustomTkinter styling
    output_resolution = ctk.CTkSlider( self, to=3, from_=0, width=134, fg_color=b, progress_color=ab, button_color=ab, button_hover_color="#006b73", number_of_steps=3, height=16 )

    match configs['Image_Size']:
      case 256: output_resolution.set(0)
      case 512: output_resolution.set(1)
      case 1024: output_resolution.set(2)
      case 2048: output_resolution.set(3)

    factory_res = ctk.CTkFrame(self, height=15, width=150, fg_color=db, corner_radius=0)
    label_font = font_details[1]
    res_256 = ctk.CTkLabel(factory_res, text="256", fg_color=db, text_color=f, font=label_font)
    res_512 = ctk.CTkLabel(factory_res, text="512", fg_color=db, text_color=f, font=label_font)
    res_1024 = ctk.CTkLabel(factory_res, text="1024", fg_color=db, text_color=f, font=label_font)
    res_2048 = ctk.CTkLabel(factory_res, text="2048", fg_color=db, text_color=f, font=label_font)

    factory_res.place(x=12, y=98)
    res_256.place(y=1)
    res_512.place(x=38, y=1)
    res_1024.place(x=72, y=1)
    res_2048.place(x=109.5, y=1)
    output_resolution.place(x=12, y=75)

    # Checkboxes for packing options with built-in text
    label_font = font_details[1]
    packing_mcpack_ch = ctk.CTkCheckBox( self, text="Convert Into .mcpack", variable=self.pack_to_mcpack_var, fg_color=ab, hover_color="#006b73", font=label_font, text_color=f, width=18, height=18, corner_radius=4 )
    packing_zip_ch = ctk.CTkCheckBox( self, text="Convert Into .zip", variable=self.pack_to_zip_var, fg_color=ab, hover_color="#006b73", font=label_font, text_color=f, width=18, height=18, corner_radius=4 )
     
    packing_mcpack_ch.place(x=225, y=65)
    packing_zip_ch.place(x=225, y=95)
  
    the_zippacker = configs['Convert_To_Zip']
    the_mcpacker = configs['Convert_To_Mcpack']
    if the_zippacker == False: packing_zip_ch.deselect()
    else: packing_zip_ch.select()
    if the_mcpacker == False: packing_mcpack_ch.deselect()
    else: packing_mcpack_ch.select()
    
    # Modern card background for output path
    output_path_bg = ctk.CTkFrame(self, fg_color=b, height=26, width=305, corner_radius=6 )
    output_folder_label = ctk.CTkLabel(self, fg_color=b, text_color=f, text="", font=font_details[1] )
    ctk.CTkLabel(self, text="Output Folder", fg_color=db, text_color=f, font=font_details[2]).place(x=12, y=5)
    ctk.CTkLabel(self, text="Sky Resolution", fg_color=db, text_color=f, font=font_details[2]).place(x=12, y=55)
    output_path_bg.place(x=77, y= 25)
    output_folder_label.place(x=82, y= 25)
    
    the_outputfolder_path = configs['Output_Folder']
    if the_outputfolder_path:
      for index in range(0, len(the_outputfolder_path), 1000):
         output_folder_label.configure(text=the_outputfolder_path[index:index+49]+"...")

    picked_options = [ output_resolution, packing_zip_ch, packing_mcpack_ch, output_folder_label ]
    option_variables = [ self.pack_to_zip_var, self.pack_to_mcpack_var ]
    settingbuttons = SettingsOptionsButtons(picked_options, self, option_variables)
    
    # Clean modern buttons with uniform aesthetic and even spacing
    btn_font = font_details[2]
    btn_w = 82
    btn_y = 145
    ctk.CTkButton(self, command=settingbuttons.ask_output_folder, text="CHANGE", 
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=60, height=24).place(x=12, y=25.2)
    ctk.CTkButton(self, command=settingbuttons.aboutprogram, text="ABOUT", 
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=26).place(x=12, y=btn_y)
    ctk.CTkButton(self, command=settingbuttons.resetsettings, text="RESET", 
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=26).place(x=105, y=btn_y)
    apply = ctk.CTkButton( self, command=settingbuttons.applysettings, text="APPLY", 
            font=btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=26 )
    apply.place(x=198, y=btn_y)
    ctk.CTkButton(self, command=settingbuttons.closesettings, text="CLOSE", 
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=btn_w, height=26).place(x=291, y=btn_y)
    ctk.CTkButton(self, command=settingbuttons.customoutres, text="OTHER", 
           font= btn_font, fg_color= ab, text_color= f, hover_color="#006b73", corner_radius=6, width=60, height=24).place(x=155, y=75)

    self.wait_window()
    self.settings_button.configure(command = lambda: SettingsWindow(self.settings_button))

   
class SettingsOptionsButtons:
    def __init__ (self, options, settingswindow, option_variables):
      self.options=options
      self.settingswindow=settingswindow
      self.settingsconfigs = ConfigManagement(options[0], option_variables[0], option_variables[1])
      
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

    def customoutres(self):
        dialog = ctk.CTkInputDialog(text="Enter Custom Resolution (min 256):", title="Custom Resolution")
        input_val = dialog.get_input()
        try:
            chosen_res = int(input_val) if input_val else 256
        except (ValueError, TypeError):
            chosen_res = 256
        if chosen_res < 256:
            chosen_res = 256
        print(chosen_res)
        self.settingsconfigs.output_res(int(chosen_res))
        
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
