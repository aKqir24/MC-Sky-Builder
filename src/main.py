import customtkinter as ctk

from worker import ToDoDuringStartup
import window

if __name__ == '__main__':
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    ToDoDuringStartup().make_temp_dir().set_defaults()
    window.MainWindow()
