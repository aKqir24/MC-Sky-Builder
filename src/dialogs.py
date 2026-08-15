import os
import customtkinter as ctk
from tkinter import messagebox

def getimageError(progresswindow):
    progresswindow.destroy()
    errormessage = "Please open an image file!!"
    messagebox.showinfo(title="No Image Found!!", message=errormessage)
