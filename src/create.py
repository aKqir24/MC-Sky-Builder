"""

    This Code Was Made By People From Stackoverflow
    I Am To Lazy To Make These Kinds Of Hard Code
    Since I'm Just A Beginer I Don't Know Many Maths

"""

from .config import *
from .worker import ResourcePackBuilder, messagebox
from .dialogs import get_image_error

import customtkinter as ctk
from time import sleep
from itertools import cycle
from tkinter import TclError
from SkyGenerator import Process
import System

class SkyImage:
    def __init__(self, progress_window, create_process, percentage):
        self.progress_window = progress_window
        self.create_process = create_process
        self.percentage = percentage

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

            pack_builder = ResourcePackBuilder()

            merged_edges = processor.MergeSkyEdges(correct_pos, blend_width, tempdir, out_extension)
            processor.SaveRgbaImage(merged_edges, save_merged)

            processor.CropMergedImage(pack_builder.old_names, save_merged, img_res, tempdir, configs['output'].get('rotate_top_bottom', True))
            pack_builder.zip_mcpack_or_both(processor.MergeJavaSky(tempdir, pack_builder.old_names, processor.inputImageSize.Width // 4, processor.inputImageSize.Width // 4)).clean_up()
        except IndexError:
            get_image_error(self.progress_window)

    create_command = lambda self: self.create()
