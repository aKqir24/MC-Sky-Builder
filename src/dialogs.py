def getimageError(self, progresswindow):
    # Handle image opening errors
    self.progresswindow.destroy()
    errormessage = "Please open an image file!!"
    messagebox.showinfo( title="No Image Found!!", message=errormessage)
    return self
