import about
from config import *
from threading import Thread
from tkinter import Toplevel, Button, Label, Scale, Checkbutton, Frame, simpledialog, BooleanVar
from worker import ToDoDuringStartup as resetto, ConfigManagement, StringVar, filedialog, rm, path, load, _tkinter

class SettingsWindow(Toplevel):  
  def __init__ (self, settingsbutton):
    super().__init__()
    self.settings_button = settingsbutton
    
  #? show the settings window
  def show(self):
    self.focus_set()
    self.title("Settings")
    self.geometry('393x181')
    self.config(background=db)
    self.resizable(False, False)
    self.iconphoto(True, PhotoImage(file=f'{title_icon_path}manufacturing.png'))
    self.settings_button.config(command=self.focus_set)

    # Resolution using, scale of the output
    output_resolution = Scale( self, to=30, from_=0, length=134, borderwidth=0, showvalue=0, bg=b2, fg=f,
                             width=10, orient='horizontal', activebackground=ab,sliderlength=20, sliderrelief= rel, 
                             troughcolor=b,resolution=10, highlightbackground=db, highlightcolor=db)

    match configs['Image_Size']:
      case 256: output_resolution.set(0)
      case 512: output_resolution.set(10)
      case 1024: output_resolution.set(20)
      case 2048: output_resolution.set(30)

    factory_res = Frame(self, height=15, width=150, bg=db, pady= 1)
    res_256 = Label(factory_res, text="256", bg=db, fg=f, pady= 1, bd=0)
    res_512 = Label(factory_res, text="512", bg=db, fg=f, pady= 1, bd=0)
    res_1024 = Label(factory_res, text="1024", bg=db, fg=f, pady= 1, bd=0)
    res_2048 = Label(factory_res, text="2048", bg=db, fg=f, pady= 1, bd=0)

    factory_res.place(x=12, y=87)
    res_256.place(y=1)
    res_512.place(x=38, y=1)
    res_1024.place(x=72, y=1)
    res_2048.place(x=109.5, y=1)
    output_resolution.place(x=10, y=74)

    # checkbox for packing options
    pack_to_zip_var = BooleanVar()
    pack_to_mcpack_var = BooleanVar()
    com = Frame(self, height=40, width=140, bg=db)
    com.place(x=242, y=65)
    packing_zip_ch = Checkbutton( com, variable=pack_to_zip_var, bg=db, fg=b2, bd=0,
                                activebackground=db, padx=-17, activeforeground=b2, relief=rel )
    
    packing_mcpack_ch = Checkbutton( com, variable=pack_to_mcpack_var, bg=db, fg=b2, bd=0,
                                activebackground=db, padx=-17, activeforeground=b2, relief=rel )
     
    packing_mcpack_ch.place(x=1)
    packing_zip_ch.place(x=1, y=22)
  
    the_zippacker = configs['Convert_To_Zip']
    the_mcpacker = configs['Convert_To_Mcpack']
    if the_zippacker == False: packing_zip_ch.deselect()
    else: packing_zip_ch.select()
    if the_mcpacker == False: packing_mcpack_ch.deselect()
    else: packing_mcpack_ch.select()
    
    # Labels for options
    output_path_bg = Frame(self, bg=b, height=26, width=305, bd=0.5 )
    output_folder_label = Label(self, bg=b, fg=f, pady=3, padx=5 )
    Label(com, text="Convert Into .zip",  bg=db, fg=f, bd=0).place(x=22, y=23)
    Label(com, text="Convert Into .mcpack", bg=db, fg=f, bd=0).place(x=22, y=1)
    Label(self, text="Output Folder", bg=db, fg=f, pady= 1, bd=0).place(x=12, y=5)
    Label(self, text="Sky Resolution", bg=db, fg=f, pady= 1, bd=0).place(x=168/3-13, y=55)
    output_path_bg.place(x=77, y= 25)
    output_folder_label.place(x=77, y= 25)
    
    the_outputfolder_path = configs['Output_Folder']
    if the_outputfolder_path:
      for index in range(0, len(the_outputfolder_path), 1000):
         output_folder_label.config(text=the_outputfolder_path[index:index+49]+"...")

    picked_options = [ output_folder_label, output_resolution, pack_to_zip_var, pack_to_mcpack_var ]
    settingbuttons = SettingsOptionsButtons( self, picked_options)
    
    # all buttons used 
    Button(self, command=settingbuttons.ask_output_folder, text="CHANGE", relief=rel, 
           padx= 5, pady= 1.5, font= font_details[0], bg= ab, fg= f, bd=1).place(x=10, y=25.2)
    Button(self, command=settingbuttons.closesettings, text="CLOSE", relief=rel, 
           padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=324.5, y=148)
    Button(self, command=settingbuttons.resetsettings, text="RESET", relief=rel, 
           padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=203, y=148)
    Button(self, command=settingbuttons.aboutprogram, text="ABOUT", relief=rel, 
           padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=10, y=148)
    Button(self, command=settingbuttons.customoutres, text="OTHER", relief=rel, 
           padx= 5, pady= 1.5, font= font_details[0], bg= ab, fg= f, bd=1).place(x=160, y=70)
    apply = Button( self, command=settingbuttons.applysettings, text="APPLY", 
            relief=rel, padx= 8, pady= 0.1, font=font_details[0], bg= ab, fg= f, bd=1 )
    apply.place(x=262.5, y=148)

    self.wait_window()
    self.settings_button.config(command = lambda: SettingsWindow(self.settings_button).show())

   
class SettingsOptionsButtons:
    def __init__ (self, settings_window, options):
      self.packzipch = options[2]
      self.packmcpackch = options[3]
      self.output_resolution = options[1]
      self.output_folder_label = options[0]
      self.settingswindow = settings_window
      self.settingsconfigs = ConfigManagement(options[1], options[2], options[3])
      
    closesettings = lambda self:self.settingswindow.destroy()
    aboutprogram = lambda self:about.aboutWin(self.settingswindow)

    def ask_output_folder(self):
      userdesktop = default_output_path()
      the_outputfolder_path = filedialog.askdirectory( initialdir=userdesktop, title="Select Output Folder" )
      self.settingsconfigs.userpath(the_outputfolder_path)
      self.settingswindow.focus_set()
      for index in range(0, len(the_outputfolder_path), 1000):
        self.output_folder_label.config(text=the_outputfolder_path[index:index+45]+"...")

    # TODO: Improve the simple dialog by making your own      
    def customoutres(self):
        chosen_res = simpledialog.askinteger( title=" ", prompt="Enter Custom Resolution?", minvalue=256 )
        if chosen_res == None: chosen_res = 256
        self.settingsconfigs.outputres(chosen_res)
        
    def resetsettings(self):
        rm(config_file)
        resetto().setdefaults()
        self.output_resolution.set(0)
        self.packzipch.deselect()
        self.packmcpackch.deselect()
        the_outputfolder_path = readconfig()[1]
        for index in range(0, len(the_outputfolder_path), 1000):
          self.output_folder_label.config(text=the_outputfolder_path[index:index+49]+"...")

    def applysettings(self):
      def savelabel():
        setsvlb = Label(self.self, bg=db, fg=f, text="Saved!!")
        setsvlb.place(x=271, y=125)
        sleep(2)
        setsvlb.destroy()

      Thread(target=self.settingsconfigs.writesettingsconfig).start()
      Thread(target=savelabel).start()
      self.settingswindow.focus_set()
