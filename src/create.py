"""

    This Code Was Made By People From Stackoverflow 
    I Am To Lazy To Make These Kinds Of Hard Code
    Since I'm Just A Beginer I Don't Know Many Maths

"""

import customtkinter as ctk
from config import *
from PIL import Image
from numpy import concatenate, array
from worker import ResourcePackBuilder, messagebox
from tkinter import TclError

class CubeMapImageProcessor:
    def __init__(self, progress_window, create_process, percentage):
        self.percentage = percentage
        self.progress_window = progress_window
        self.create_process = create_process

    def no_image_handler(self):
        from convert import SkyImageConverter
        return SkyImageConverter.getimageError(self)

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
        """Blends the edges of Top, Front, and Bottom images into a smooth seam."""
        top = Image.open(tempdir + 'Top' + ext).rotate(-180)
        front = Image.open(tempdir + 'Front' + ext)
        bottom = Image.open(tempdir + 'Bottom' + ext).rotate(180)

        combined_height = top.height * 3
        mrg = Image.new("RGBA", (top.width, combined_height))
        mrg.paste(top)
        mrg.paste(front, (0, top.height))
        mrg.paste(bottom, (0, top.height * 2))

        left = mrg.crop((0, 0, top.width // 2, combined_height))
        right = mrg.crop((top.width // 2, 0, top.width, combined_height))

        combined = Image.fromarray(concatenate((array(left), array(right)), axis=1))

        for i in range(blend_width):
            alpha = i / blend_width
            for y in range(combined_height):
                x1 = clip(left.width - blend_width + i, 0, left.width - 1)
                x2 = clip(blend_width - i, 0, right.width - 1)

                p1 = left.getpixel((x1, y))
                p2 = right.getpixel((x2, y))

                blended_pixel = tuple(int((1 - alpha) * a + alpha * b) for a, b in zip(p1, p2))
                px = top.width // 2 - blend_width + i + correct_position
                combined.putpixel((px, y), blended_pixel)

        return combined

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
            """Crop blended sky into top, front, bottom and save them."""
            image = Image.open(merged_path)
            coords = [
                (0, 0, img_res, img_res),
                (0, img_res, img_res, img_res * 2),
                (0, img_res * 2, img_res, img_res * 3)
            ]
            name_indices = [4, 2, 5]

            for i, box in enumerate(coords):
                path = tempdir + old_names[name_indices[i]]
                rm(path)
                cropped = image.crop(box)
                if (i == 0 or i == 2) and export_config[3] is True:
                    cropped = cropped.rotate(180)
                cropped.save(path)
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
            img_res, out_path = export_config[0], export_config[1]
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
