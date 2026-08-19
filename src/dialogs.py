import os
import customtkinter as ctk
import ctkmessagebox2 as messagebox

def get_image_error(progress_window):
    errormessage = "Please open an image file!!"
    messagebox.showinfo(progress_window, title="No Image Found!!", message=errormessage)
    progress_window.destroy()
