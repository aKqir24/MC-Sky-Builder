import about
from all_val import *
from time import sleep as time_sleep
from create import Thread, CreateCubeIMG, Image, ImageTk
from tkinter import Toplevel, Button, Label, Scale, Checkbutton, Frame, simpledialog, messagebox, BooleanVar
from worker import ToDoDuringStartup as resetto, SettingsMultiOptions, ConfigManagement, StringVar, filedialog, winreg, rm, path, load, _tkinter

class SettingsWindow:  
  def __init__ (self, settingsbutton):
    self.settingsbutton = settingsbutton
    
  # settings (Settings Window Of The Program )
  def loadsettings(self):
    settingswindow = Toplevel()
    settingswindow.focus_set()
    settingswindow.title("Settings")
    settingswindow.geometry('393x181')
    settingswindow.config(background=db)
    settingswindow.resizable(False, False)
    settingswindow.iconbitmap('res\\title\\manufacturing.ico')
    self.settingsbutton.config(command=settingswindow.focus_set)

    def scalelabel():
      # settings ( Resolution Using, Scale Of The Output )
      imgresolution = Scale( settingswindow, to=30, from_=0, length=134, borderwidth=0, showvalue=0, bg=b2, fg=f,
                             width= 10, orient='horizontal', activebackground=ab,sliderlength=20, sliderrelief= rel, 
                             troughcolor=b,resolution=10, highlightbackground=db, highlightcolor=db)

      with open(config_dir,'r') as readconfig:
        readusingjson = load(readconfig)
        the_chosen_res = readusingjson['Image_Size']
        if the_chosen_res == 256: imgresolution.set(0)
        elif the_chosen_res == 512: imgresolution.set(10)
        elif the_chosen_res == 1024: imgresolution.set(20)
        elif the_chosen_res == 2048: imgresolution.set(30)

      factory_res = Frame(settingswindow, height=15, width=150, bg=db, pady= 1)
      res_256 = Label(factory_res, text="256", bg=db, fg=f, pady= 1, bd=0)
      res_512 = Label(factory_res, text="512", bg=db, fg=f, pady= 1, bd=0)
      res_1024 = Label(factory_res, text="1024", bg=db, fg=f, pady= 1, bd=0)
      res_2048 = Label(factory_res, text="2048", bg=db, fg=f, pady= 1, bd=0)

      factory_res.place(x=12, y=87)
      res_256.place(y=1)
      res_512.place(x=38, y=1)
      res_1024.place(x=72, y=1)
      res_2048.place(x=109.5, y=1)
      imgresolution.place(x=10, y=74)

      def outoptions():
        packing_zip_val = BooleanVar()
        packing_mcpack_val = BooleanVar()
        com = Frame(settingswindow, height=40, width=140, bg=db)
        com.place(x=242, y=65)
        packing_zip_ch = Checkbutton( com, variable=packing_zip_val, bg=db, fg=b2, bd=0,
                                    activebackground=db, padx=-17, activeforeground=b2, relief=rel )
        
        packing_mcpack_ch = Checkbutton( com, variable=packing_mcpack_val, bg=db, fg=b2, bd=0,
                                    activebackground=db, padx=-17, activeforeground=b2, relief=rel )
         
        packing_mcpack_ch.place(x=1)
        packing_zip_ch.place(x=1, y=22)
  
        with open(config_dir,'r') as readconfig:
          readusingjson =  load(readconfig)
          the_zippacker = readusingjson['Convert_To_Zip']
          the_mcpacker = readusingjson['Convert_To_Mcpack']
          if the_zippacker == False: packing_zip_ch.deselect()
          elif the_zippacker == True: packing_zip_ch.select()
          if the_mcpacker == False: packing_mcpack_ch.deselect()
          elif the_mcpacker == True: packing_mcpack_ch.select()

        def optionlabels():
          output_path_bg = Frame(settingswindow, bg=b, height=26, width=305, bd=0.5 )
          outputfolderlabel = Label(settingswindow, bg=b, fg=f, pady=3, padx=5 )
          Label(com, text="Convert Into .zip",  bg=db, fg=f, bd=0).place(x=22, y=23)
          Label(com, text="Convert Into .mcpack", bg=db, fg=f, bd=0).place(x=22, y=1)
          Label(settingswindow, text="Output Folder", bg=db, fg=f, pady= 1, bd=0).place(x=12, y=5)
          Label(settingswindow, text="Sky Resolution", bg=db, fg=f, pady= 1, bd=0).place(x=168/3-12, y=55)
          output_path_bg.place(x=77, y= 25)
          outputfolderlabel.place(x=77, y= 25)
      
          with open(config_dir, 'r') as readconfig:
            readusingjson = load(readconfig)
            the_outputfolder_path = readusingjson['Outputfolder_Path']
            if the_outputfolder_path:
              for index in range(0, len(the_outputfolder_path), 1000):
                outputfolderlabel.config(text=the_outputfolder_path[index:index+49]+"...")

          user_options = SettingsMultiOptions(imgresolution, packing_zip_val, packing_mcpack_val)
          settingbuttons = SettingsOptionsButtons(settingswindow, outputfolderlabel, user_options, imgresolution, packing_zip_ch, packing_mcpack_ch)

          def optionbuttons():
            Button(settingswindow, command=settingbuttons.ask_output_folder, text="CHANGE", relief=rel, 
                   padx= 5, pady= 1.4, font= font_details[0], bg= ab, fg= f, bd=1).place(x=10, y=25.2)
            Button(settingswindow, command=settingbuttons.closesettings, text="CLOSE", relief=rel, 
                   padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=324.5, y=148)
            Button(settingswindow, command=settingbuttons.resetsettings, text="RESET", relief=rel, 
                   padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=203, y=148)
            Button(settingswindow, command=settingbuttons.aboutprogram, text="ABOUT", relief=rel, 
                   padx= 8, pady= 0.1, font= font_details[0], bg= ab, fg= f, bd=1).place(x=10, y=148)
            Button(settingswindow, command=settingbuttons.customoutres, text="OTHER", relief=rel, 
                   padx= 5, pady= 1.4, font= font_details[0], bg= ab, fg= f, bd=1).place(x=160, y=70)
            apply = Button( settingswindow, command=settingbuttons.applysettings, text="APPLY", 
                    relief=rel, padx= 8, pady= 0.1, font=font_details[0], bg= ab, fg= f, bd=1 )
            apply.place(x=262.5, y=148)

            def afterclosing():
              try: 
                settingswindow.wait_window()
                self.settingsbutton.config(command=SettingsWindow(self.settingsbutton).loadsettings)
              except _tkinter.TclError: pass

            return afterclosing()
          return optionbuttons()
        return optionlabels()          
      return outoptions()
    return scalelabel()
   
class SettingsOptionsButtons:
    def __init__ (self, settingswindow, outfollbl, usropts, imgres, packzipch, packmcpackch):
      self.imgresolution = imgres
      self.user_options = usropts
      self.packzipch = packzipch
      self.packmcpackch = packmcpackch
      self.outputfolderlabel = outfollbl
      self.settingswindow = settingswindow
      
    closesettings = lambda self:self.settingswindow.destroy()
    aboutprogram = lambda self:about.aboutWin(self.settingswindow)

    def ask_output_folder(self):
      with winreg.OpenKey(winreg.HKEY_CURRENT_USER, dsktp_regkey) as key:
        userdesktop = path.expandvars( winreg.QueryValueEx(key, "Desktop")[0] )
      the_outputfolder_path = filedialog.askdirectory( initialdir=userdesktop, title="Select Output Folder" )
      ConfigManagement().OutPathConfigValue(the_outputfolder_path)
      self.settingswindow.focus_set()
      for index in range(0, len(the_outputfolder_path), 1000):
        self.outputfolderlabel.config(text=the_outputfolder_path[index:index+49]+"...")
          
    def customoutres(self):
        chosen_res = simpledialog.askinteger( title="", prompt="", minvalue=1 )
        if chosen_res == None: chosen_res = 256
        ConfigManagement().CustomImgResConfigValue(chosen_res)
        
    def resetsettings(self):
        rm(config_dir)
        resetto().setdefaults()
        self.imgresolution.set(0)
        self.packzipch.deselect()
        self.packmcpackch.deselect()
        with open(config_dir, 'r') as readconfig:
          readusingjson = load(readconfig)
          the_outputfolder_path = readusingjson['Outputfolder_Path']
          for index in range(0, len(the_outputfolder_path), 1000):
              self.outputfolderlabel.config(text=the_outputfolder_path[index:index+49]+"...")

    def applysettings(self):
      def savelabel():
        setsvlb = Label(self.settingswindow, bg=db, fg=f, text="Saved!!")
        setsvlb.place(x=271, y=125)
        time_sleep(3)
        setsvlb.destroy()

      Thread(target=ConfigManagement().writesettingsconfig).start()
      self.user_options.checkmcpackconvert()
      self.user_options.checkzipconvert()
      Thread(target=savelabel).start()
      self.settingswindow.focus_set()
      self.user_options.outputres()
