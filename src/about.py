from tkinter import Tk, Toplevel

class AboutWindow(Toplevel):
   def __init__ (self):
       super().__init__()

   def show(self):
      aboutwindow = Toplevel()
      aboutwindow.geometry('350x400')
      aboutwindow.title("About") 
      aboutwindow.destroy() 
