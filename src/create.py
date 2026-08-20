"""

    This Code Was Made By People From Stackoverflow
    I Am To Lazy To Make These Kinds Of Hard Code
    Since I'm Just A Beginer I Don't Know Many Maths

"""

from .config import *
from .worker import ResourcePackBuilder, messagebox
from .dialogs import StatusMessage

import customtkinter as ctk
from time import sleep
from itertools import cycle
from tkinter import TclError
from SkyGenerator import Process
import System

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
            processor.InitializeImages()
            pv, correct_pos, blend_width = processor.OutputValues(processor.inputImageSize, configs['output']['edge_blend'])

            def update_ui_progress(val):
                try:
                    self.percentage.set(f"{int(val)}%")
                    self.create_process.set(val / 100.0)
                    self.progress_window.update_idletasks()
                except Exception:
                    pass

            progress_action = System.Action[System.Double](update_ui_progress)
            progress_value = processor.ConvertBack(pv, 1.0, configs['output']['curvature'], progress_action)
            save_merged = f"{tempdir}combined.png"
            processor.SaveOutputImage(f"{tempdir}output_sky.png")

            img_res = configs['output']['resolution']
            remaining_progress = (100 - progress_value) / 12 + 0.01
            progress_value = processor.ExportFaces(int(img_res), tempdir, remaining_progress, progress_value, progress_action)

            merged_edges = processor.MergeSkyEdges(correct_pos, blend_width, tempdir, out_extension)
            processor.SaveRgbaImage(merged_edges, save_merged)

            pack_builder = ResourcePackBuilder()
            processor.CropMergedImage(pack_builder.old_names, save_merged, img_res, tempdir, configs['output'].get('rotate_top_bottom', True))
            pack_builder.zip_mcpack_or_both(processor.MergeJavaSky(tempdir, pack_builder.old_names, processor.inputImageSize.Width // 4, processor.inputImageSize.Width // 4)).clean_up()
        except IndexError:
            StatusMessage.get_image_error(self.progress_window)

    create_command = lambda self: self.create()
