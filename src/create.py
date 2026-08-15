"""

    This Code Was Made By People From Stackoverflow
    I Am To Lazy To Make These Kinds Of Hard Code
    Since I'm Just A Beginer I Don't Know Many Maths

"""


from .config import *
from .worker import ResourcePackBuilder, messagebox

import customtkinter as ctk
from PIL import Image
from numpy import concatenate, array
from time import sleep
from tkinter import TclError

class CubeMapImageProcessor:
    def __init__(self, progress_window, create_process, percentage):
        self.percentage = percentage
        self.progress_window = progress_window
        self.create_process = create_process

    def no_image_handler(self):
        from convert import SkyImageConverter
        return SkyImageConverter.getimageError(self.progress_window)

    noimagehandler = no_image_handler
    getcreatesky = lambda self: self.get_create_sky()

    def loading_title(self):
        """Updates the progress window title while building the sky."""
        try:
            sleep(1)
            while int(self.percentage.get().replace("%", "")) < 100:
                for i, dots in enumerate([" ", ".", "..", "...", "...", "..", "."]):
                    if int(self.percentage.get().replace("%", "")) >= 100:
                        self.progress_window.destroy()
                        messagebox.showinfo("Finished!", "Sky `Building` was a success :D")
                        return
                    self.progress_window.title(f"Building Sky{dots}")
                    sleep(1)
        except (TclError, RuntimeError, ValueError):
            pass

    def merge_sky_edges(self, correct_position, blend_width):
        """Blends the edges of Top, Front, and Bottom images into a smooth seam using vectorized NumPy operations."""
        top = Image.open(tempdir + 'Top' + out_extension).rotate(-180)
        front = Image.open(tempdir + 'Front' + out_extension)
        bottom = Image.open(tempdir + 'Bottom' + out_extension).rotate(180)

        combined_height = top.height * 3
        mrg = Image.new("RGBA", (top.width, combined_height))
        mrg.paste(top)
        mrg.paste(front, (0, top.height))
        mrg.paste(bottom, (0, top.height * 2))

        left = mrg.crop((0, 0, top.width // 2, combined_height))
        right = mrg.crop((top.width // 2, 0, top.width, combined_height))

        left_arr = array(left)
        right_arr = array(right)
        combined_arr = concatenate((left_arr, right_arr), axis=1)

        if blend_width > 0:
            import numpy as np
            alpha_bc = np.linspace(0.0, 1.0, blend_width, endpoint=True)[None, :, None]

            x1_indices = np.clip(np.arange(left.width - blend_width, left.width), 0, left.width - 1)
            x2_indices = np.clip(np.arange(blend_width - 1, -1, -1), 0, right.width - 1)

            p1 = left_arr[:, x1_indices, :]
            p2 = right_arr[:, x2_indices, :]

            blended = ((1.0 - alpha_bc) * p1 + alpha_bc * p2).astype('uint8')

            dest_start = top.width // 2 - blend_width + correct_position
            dest_end = dest_start + blend_width

            combined_arr[:, dest_start:dest_end, :] = blended

        return Image.fromarray(combined_arr)

    def merge_java_sky(self):
        """Creates a Java-style sky layout (3x2 grid)."""
        filenames = PackingPack.old_names
        images = [Image.open(tempdir + filenames[i]) for i in [5, 4, 0, 1, 2, 3]]

        width, height = images[0].size
        canvas = Image.new("RGBA", (width * 3, height * 2))

        for i, img in enumerate(images):
            x = (i if i < 3 else i - 3) * width
            y = 0 if i < 3 else height
            canvas.paste(img, (x, y))

        return canvas

    def get_create_sky(self):
        """Main method to handle full sky conversion, blending, cropping, and packing."""

        def crop_merged_image(old_names, merged_path):
            """Crop blended sky into top, front, bottom and save them securely."""
            coords = [
                (0, 0, img_res, img_res),
                (0, img_res, img_res, img_res * 2),
                (0, img_res * 2, img_res, img_res * 3)
            ]
            name_indices = [4, 2, 5]

            with Image.open(merged_path) as image:
                for i, (box, idx) in enumerate(zip(coords, name_indices)):
                    path = tempdir + old_names[idx]
                    if path.exists if hasattr(path, 'exists') else __import__('os').path.exists(path):
                        try:
                            rm(path)
                        except OSError:
                            pass
                    cropped = image.crop(box)
                    if (i == 0 or i == 2) and configs['output'].get('rotate_top_bottom', True):
                        cropped = cropped.rotate(180)
                    cropped.save(path)
            if __import__('os').path.exists(merged_path):
                rm(merged_path)

        try:
            export_config = readconfig()
            self.progress_window.focus_set()

            img_in = Image.open(image_details[0])
            width, height = img_in.size
            img_out = Image.new("RGB", (width, int(width * 3 / 4)), "black")

            from convert import SkyImageConverter
            converter = SkyImageConverter(img_in, img_out, self.progress_window, self.create_process, self.percentage)
            pv, correct_pos, blend_width = converter.OutputValues((width, height))
            progress_value = converter.convertBack(pv)
            packsky = ResourcePackBuilder

            name_map = [
                ["", "", "Top", ""],
                ["Front", "Right", "Back", "Left"],
                ["", "", "Bottom", ""]
            ]

            cube_size = width / 4
            img_res = configs['output']['resolution']
            save_merged = tempdir + 'combined.png'

            for row in range(3):
                for col in range(4):
                    name = name_map[row][col]
                    if name:
                        x = col * cube_size
                        y = row * cube_size
                        region = img_out.crop((x, y, x + cube_size, y + cube_size))
                        region = region.resize((int(img_res), int(img_res)))
                        region.save(tempdir + name + ".png")
                        converter.CurrentProgress(pv, progress_value)

            remaining = 100 - progress_value
            step = remaining / 3

            for phase in range(1, 5):
                if phase == 4:
                    sleep(1)
                else:
                    converter.CurrentProgress(pv, progress_value + step * phase)
                    if phase == 1:
                        self.merge_sky_edges(correct_pos, blend_width).save(save_merged)
                    elif phase == 2:
                        crop_merged_image(packsky.old_names, save_merged)
                    elif phase == 3:
                        packsky().zip_mcpack_or_both(self.merge_java_sky()).clean_up()

        except (IndexError, TclError):
            self.no_image_handler()
