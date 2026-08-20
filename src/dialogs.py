import ctkmessagebox2 as messagebox

class StatusMessage:
    def __init__(self, window):
        self.window = window

    def get_image_error(self, destroy_window=False):
        errormessage = "Please open an image file!!"
        messagebox.showinfo(self.window, title="No Image Found!!", message=errormessage)
        if destroy_window == True: self.window.destroy()
