"""
  Distributes the default ''Elements'' used, in the modules
"""

import os
import subprocess
from json import dump
from pathlib import Path
from tempfile import gettempdir

# 1. Resolve Platform-Specific Handlers Once at Startup
def _init_platform():
    home = Path.home()
    if os.name == "nt":
        cfg_folder = Path(os.getenv("APPDATA", home / "AppData/Roaming")) / "mcskymaker"
        opener = lambda folder: subprocess.Popen(["explorer", folder])

        # Try fetching Windows Desktop folder via registry efficiently
        desktop = home / "Desktop"
        try:
            from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
            with OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
                desktop = Path(os.path.expandvars(QueryValueEx(key, "Desktop")[0]))
        except Exception:
            pass
        return cfg_folder, opener, desktop

    elif os.name == "posix":
        cfg_folder = home / ".mcskymaker"
        opener = lambda folder: subprocess.Popen(["xdg-open", folder])
        desktop = home / "Desktop"
        if not desktop.exists():
            desktop = home
        return cfg_folder, opener, desktop
    else:
        raise SystemExit("ERR: OS is not supported!")

# 2. Assign Immutable Constants (Static after initial import)
config_folder, open_folder, default_output_path = _init_platform()
config_file = config_folder / "config.json"
tempdir = f"{gettempdir()}/MC-Sky-Builder"

#? details config input values
image_details: list = []
out_extension: str = ".png"
configs = {
    "settings": {
        "output_folder": str(default_output_path),
        "auto_save": False,
        "ask_pack_name": True,
        "export_mcpack": False,
        "export_zip": False
    },
    "output": {
        "resolution": 256,
        "curvature": 2.14,
        "edge_blend": 50,
        "saturation": 0,
        "rotate_top_bottom": True
    }
}

# interface values
default_resolutions = [256, 512, 1024, 2048]
noto_font = 'resource/noto_sans.ttf'
try: noto_font_name = ImageFont.truetype(noto_font, 9).getname()[1]
except Exception: noto_font_name = "sans-serif"

font_details = [
    (noto_font_name, 10, 'normal'),
    (noto_font_name, 11, 'normal'),
    (noto_font_name, 11, 'bold'),
    (noto_font_name, 13, 'normal'),
    (noto_font_name, 13, 'bold')
]
title_icon_path = 'resource/title'

# functions used globally
def change_path_label(label, input_path=None, length=55):
    if input_path is None:
        input_path = configs['settings']['output_folder']
    if input_path:
      for index in range(0, len(input_path), 1000):
        label.configure(text=input_path[index:index+length]+"...")

def readconfig():
  if os.path.exists(config_file):
      try:
          with open(config_file, 'r') as raw_config:
            json_open = load(raw_config)
            for key in configs:
                if key in json_open:
                    if isinstance(configs[key], dict) and isinstance(json_open[key], dict):
                        configs[key].update(json_open[key])
                    else:
                        configs[key] = json_open[key]
      except Exception:
          pass
  return configs

def writeconfig():
    with open(config_file, 'w') as raw_config:
        dump(configs, raw_config, indent=4)
