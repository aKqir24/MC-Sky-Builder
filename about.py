from tkinter import Tk, Toplevel

def aboutWin(settingswindow):
  aboutwindow = Toplevel()
  aboutwindow.geometry('350x400')
  aboutwindow.title("About")
  settingswindow.wait_window()
  aboutwindow.destroy() 