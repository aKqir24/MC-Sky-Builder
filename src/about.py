from .config import *
from PIL import Image
import customtkinter as ctk
import webbrowser

class AboutWindow(ctk.CTkToplevel):
   def __init__ (self):
        super().__init__()
        self.geometry('444x430')
        self.minsize(444, 430)
        self.resizable(False, False)
        self.title("About MC Sky Builder")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        try:
            self.iconbitmap(f'{title_icon_path}app.ico')
        except Exception:
            pass

        # Header / Logo
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(16, 8), sticky="n")
        
        self.about_icon = ctk.CTkImage(dark_image=Image.open(str(RESOURCE_DIR / "actions" / "about.png")), size=(40, 40))
        ctk.CTkLabel(header_frame, image=self.about_icon, text="  MC Sky Builder", font=font_details[4], compound="left").pack(anchor="center")

        # Tabview for About and License
        tabview = ctk.CTkTabview(self, width=396, height=240)
        tabview.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="news")
        
        tab_about = tabview.add("About")
        tab_license = tabview.add("License")

        # About Tab Textbox
        tab_about.grid_columnconfigure(0, weight=1)
        tab_about.grid_rowconfigure(0, weight=1)
        des_textbox = ctk.CTkTextbox(tab_about, font=font_details[1], fg_color=("#e8f5e9", "#18271a"), activate_scrollbars=True)
        des_textbox.grid(row=0, column=0, sticky="news")
        
        with open(str(RESOURCE_DIR / "about.txt"), "r", encoding="utf-8") as about_msg:
            des_textbox.insert("0.0", about_msg.read())
            des_textbox.configure(state="disabled")

        # License Tab Textbox
        tab_license.grid_columnconfigure(0, weight=1)
        tab_license.grid_rowconfigure(0, weight=1)
        lic_textbox = ctk.CTkTextbox(tab_license, font=font_details[1], fg_color=("#e8f5e9", "#18271a"), activate_scrollbars=True)
        lic_textbox.grid(row=0, column=0, sticky="news")
        
        try:
            license_path = Path(__file__).resolve().parent.parent / "LICENSE"
            with open(license_path, "r", encoding="utf-8") as lf:
                lic_text = lf.read()
        except Exception:
            lic_text = "MIT License - Free for Open Source projects."
        lic_textbox.insert("0.0", lic_text)
        lic_textbox.configure(state="disabled")

        # Action Buttons Frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=24, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        btn_font = font_details[2]
        ctk.CTkButton(btn_frame, text="GitHub", font=btn_font, height=30, command=lambda: webbrowser.open("https://github.com/aKqir24/MC-Sky-Builder")).grid(row=0, column=0, padx=4, sticky="ew")
        ctk.CTkButton(btn_frame, text="Star ⭐", font=btn_font, height=30, command=lambda: webbrowser.open("https://github.com/aKqir24/MC-Sky-Builder/stargazers")).grid(row=0, column=1, padx=4, sticky="ew")
        ctk.CTkButton(btn_frame, text="Close", font=btn_font, height=30, fg_color="gray50", hover_color="gray40", command=self.destroy).grid(row=0, column=2, padx=4, sticky="ew")
