from .config import *
import customtkinter as ctk

class AboutWindow(ctk.CTkToplevel):
   def __init__ (self):
        super().__init__()
        self.geometry('450x500')
        self.resizable(False, False)
        self.title("About")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Widget Containers
        header_container = ctk.CTkFrame(self, height=88, width=400)
        header_container.grid(row=0, column=0, padx=2, pady=2, sticky="wne")

        # About description textbox
        about_des = """
        Hello, I am Akqir(aKqir24) the one who made this program.
        And here in this about window, I will tell you about this program I made.
        It started when I was editing a sky overlay for MC and I always automate
        stuff in python especially the time I am edited a sky overlay pack, which
        was never released.
        """
        textbox_wrapper = ctk.CTkFrame(self)
        textbox_wrapper.grid(row=1, column=0, sticky="wens")
        des_textbox = ctk.CTkTextbox(textbox_wrapper, activate_scrollbars=False, width=352)
        des_textbox.grid(row=1, column=0, sticky="wsew")
        des_textbox_scrollbar = ctk.CTkScrollbar(textbox_wrapper, command=des_textbox.yview)
        des_textbox_scrollbar.grid(row=1, column=1, sticky="e")
        des_textbox.configure(yscrollcommand=des_textbox_scrollbar.set)
        des_textbox.insert("0.0", about_des)
        des_textbox.configure(state="disabled")
