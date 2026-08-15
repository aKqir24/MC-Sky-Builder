import customtkinter as ctk
from customtkinter.windows.widgets.font import FontManager
FontManager.linux_font_path = "/tmp/.fonts/"

from .worker import EnvironmentInitializer
from . import window

if __name__ == '__main__':
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("theme.json")

    EnvironmentInitializer().make_temp_dir().set_defaults()
    window.SkyBuilderWindow()
