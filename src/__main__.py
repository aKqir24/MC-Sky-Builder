import os
import sys
import pythonnet
pythonnet.load("coreclr")
import clr

generator_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generator")
if generator_dir not in sys.path:
    sys.path.append(generator_dir)

dll_path = os.path.join(generator_dir, "generator.dll")
clr.AddReference(dll_path)

import customtkinter as ctk
from customtkinter.windows.widgets.font import FontManager
from .worker import EnvironmentInitializer
from .config import RESOURCE_DIR
from . import window

FontManager.linux_font_path = f"{tempdir}.fonts/"

if __name__ == '__main__':
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(str(RESOURCE_DIR / "theme.json"))

    EnvironmentInitializer().make_temp_dir().set_defaults()
    window.SkyBuilderWindow()
