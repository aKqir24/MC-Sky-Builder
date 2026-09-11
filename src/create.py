from .config import *
from .worker import ResourcePackBuilder
from .dialogs import StatusMessage

import customtkinter as ctk
import ctkmessagebox2 as messagebox
from time import sleep
from itertools import cycle
from tkinter import TclError
from SkyGenerator import Process
import System
from PIL import Image, ImageEnhance
from os import path

class UpdateWindow:
    def __init__(self, create_btn=None):
        self.create_btn = create_btn
        self.percentage = ctk.StringVar()
        self.percentage.set("0%")

        self.progress_window = ctk.CTkToplevel()
        self.progress_window.geometry('420x110')
        self.progress_window.minsize(424, 110)
        self.progress_window.title("Building Sky")
        self.progress_window.resizable(False, False)
        try: self.progress_window.iconbitmap(f'{title_icon_path}conversion.ico')
        except Exception: pass

        self.create_process = ctk.CTkProgressBar(self.progress_window, width=380, height=14)
        self.create_process.set(0)
        self.create_process.place(x=20, y=25)

        label = ctk.CTkLabel(self.progress_window, textvariable=self.percentage, font=font_details[2])
        label.place(x=420/2 - 20, y=65)

        self.progress_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        if self.create_btn:
            try: self.create_btn.configure(command=self.progress_window.focus_set)
            except Exception: pass

    def loading_title(self):
        """Updates the progress window title while building the sky."""
        try:
            sleep(1)
            for dots in cycle(["", ".", "..", "...", "...", "..", "."]):
                if int(self.percentage.get().replace("%", "")) >= 100:
                    messagebox.showinfo(self.progress_window, "Finished!", "Sky `Building` was a success :D")
                    self.progress_window.destroy()
                    break
                self.progress_window.title(f"Building Sky{dots}")
                sleep(1)
        except (TclError, RuntimeError, ValueError):
            pass

    def on_closing(self):
        ResourcePackBuilder().clean_up()
        try:
            self.progress_window.destroy()
        except Exception:
            pass

class SkyImage(UpdateWindow):
    def __init__(self, create_btn=None):
        super().__init__(create_btn)

    def create(self):
        try:
            processor = Process(image_details[0])

            def update_ui_progress(val):
                try:
                    print(float(val))
                    self.percentage.set(f"{int(val)}%")
                    self.create_process.set(val / 100.0)
                    self.progress_window.update_idletasks()
                except Exception:
                    pass

            progress_action = System.Action[System.Double](update_ui_progress)
            img_res = int(configs['output']['resolution'])

            java_sky_img = processor.ProcessSky(
                lambda mode, size, color: Image.new(mode, tuple(size), tuple(color)),
                lambda mode, size, data: Image.frombytes(mode, tuple(size), bytes(data), "raw", mode, 0, 1),
                lambda p: Image.open(p),
                lambda im, factor: ImageEnhance.Color(im).enhance(factor),
                lambda im, box: im.crop(tuple(box)),
                lambda im, size, res: im.resize(tuple(size), res),
                lambda im, other, xy: im.paste(other, tuple(xy)),
                hasattr(Image, 'Resampling'),
                Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else None,
                Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else None,
                image_details[0],
                tempdir,
                out_extension,
                img_res,
                configs['output']['edge_blend'],
                configs['output']['curvature'],
                configs['output']['saturation'],
                configs['output'].get('rotate_top_bottom', True),
                progress_action
            )

            pack_builder = ResourcePackBuilder()
            pack_builder.zip_mcpack_or_both(java_sky_img).clean_up()
        except IndexError:
            StatusMessage.get_image_error(self.progress_window)

    create_command = lambda self: self.create()
