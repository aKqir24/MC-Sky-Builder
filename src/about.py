import customtkinter as ctk

class AboutWindow(ctk.CTkToplevel):
   def __init__ (self):
       super().__init__()

   def show(self):
      aboutwindow = ctk.CTkToplevel()
      aboutwindow.geometry('350x400')
      aboutwindow.title("About") 
      aboutwindow.destroy() 
