"""
    Worker works around with Files, and Directory

 - setting the configuration file, ui, and directory
 - creating or preparing the temporary files needed
 - managing the filenames, extension and other details
 - zipping the complete output of create

"""

from .config import *

from shutil import copytree, copy, move, rmtree, make_archive
import ctkmessagebox2 as messagebox
from os import path, mkdir
from json import dump
from SkyGenerator import Process
from time import strftime

class GetImageDetails:
    def __init__(self, imgpath):
        self.imgpath = imgpath

    def get_image_name(self):
        # Get file extension and filename without extension
        img_ext = self.get_img_ext()
        base_path = self.imgpath.replace('jpg', 'jpeg').replace(img_ext, "")
        filename = path.basename(base_path)
        image_details.append(filename)
        return filename

    def get_img_ext(self):
        # Open image and get extension
        img_format = Process.GetImageFormat(self.imgpath)
        ext = "." + img_format.lower()
        image_details.append(ext)
        return ext

class EnvironmentInitializer:
    def make_temp_dir(self):
        if not path.exists(tempdir):
            mkdir(tempdir)
        if not path.exists(config_folder):
            mkdir(config_folder)
        return self

    def set_defaults(self):
        if not path.exists(config_file):
            writeconfig()
        readconfig()
        return self

class ConfigurationManager:
    def __init__(self, output_resolution, pack_zip_val, pack_mcpack_val):
        self.output_resolution = output_resolution
        self.pack_zip_val = pack_zip_val
        self.pack_mcpack_val = pack_mcpack_val
        self.stored_config = configs
        self.custom_recent_resolution = None
        self.scale_recent_resolution = None

    def userpath(self, folder):
        self.stored_config["settings"].update({"output_folder": folder})

    def output_res(self, resolution):
        scale_res = self.output_resolution.get()
        if resolution > 4 and resolution is not None:
            chosen_resolution = resolution
            self.custom_recent_resolution = resolution
        elif supported_resolutions.get(resolution) and self.scale_recent_resolution != supported_resolutions[resolution]:
            chosen_resolution = supported_resolutions[resolution]
            self.custom_recent_resolution = None
        else:
            chosen_resolution = self.custom_recent_resolution if self.custom_recent_resolution else supported_resolutions.get(resolution, resolution)
        self.scale_recent_resolution = supported_resolutions.get(scale_res, scale_res)
        self.stored_config["output"].update({"resolution": chosen_resolution})

    def write_settings_config(self):
        self.output_res(self.output_resolution.get())
        self.stored_config["settings"].update({
            "export_zip": self.pack_zip_val.get(),
            "export_mcpack": self.pack_mcpack_val.get()
        })
        writeconfig()

class PackManifestGenerator:
    pack_description = "This SkyOverlay Was Made By Using §cAkqir's §f(§bMC §fSky Builder) Software..."
    pack_name = lambda self: image_details[2] + " (Sky Overlay)"
    mcpack_file = lambda self: self.pack_name() + ".mcpack"
    zippack_file = lambda self: self.pack_name() + ".zip"

    def make_manifest(self):
        from uuid import uuid4
        manifest = {
            "format_version": 1,
            "header": {
                "description": self.pack_description,
                "name": self.pack_name(),
                "uuid": str(uuid4()),
                "version": [1, 0, 0],
                "min_engine_version": [1, 12, 0]
            },
            "modules": [{
                "description": "",
                "type": "resources",
                "uuid": str(uuid4()),
                "version": [1, 0, 0]
            }]
        }
        manifest_path = path.join(tempdir, self.mcpack_file(), 'manifest.json')
        with open(manifest_path, 'w') as f:
            dump(manifest, f, sort_keys=True, indent=3)
        return self

    def make_pack_meta(self):
        pack_description_clean = self.pack_description.replace("§c", "").replace("§b", "").replace("§f", "")
        meta = {
            "pack": {
                "pack_format": 1,
                "description": pack_description_clean
            }
        }
        meta_path = path.join(tempdir, self.zippack_file(), 'pack.mcmeta')
        with open(meta_path, 'w') as f:
            dump(meta, f, sort_keys=True, indent=3)
        return self

    def make_pack_icon(self, image_right, pack_folder, pack_icon_name):
        src = path.join(tempdir, image_right)
        dst = path.join(tempdir, pack_folder, pack_icon_name)
        copy(src, dst)

class ResourcePackBuilder(PackManifestGenerator):
    def __init__(self):
        super().__init__()
        self.old_names = ["Back.png", "Left.png", "Front.png", "Right.png", "Top.png", "Bottom.png"]
        self.new_names = [f"cubemap_{i}.png" for i in range(6)]

    def move_to_out(self, pack_filename):
        finished_path = path.join(tempdir, pack_filename)
        output_path = path.join(configs['settings']['output_folder'].replace("/", "\\"), pack_filename)
        make_archive(output_path, 'zip', path.dirname(finished_path))
        if pack_filename.endswith(".zip"):
            move(output_path + ".zip", output_path.replace(".zip", ""))
        else:
            move(output_path + ".zip", output_path)
        return self

    def clean_up(self):
        print("Cleaning up TEMP files...")
        tempdir_path = tempdir[:-1] if tempdir.endswith("\\") else tempdir
        if path.exists(tempdir_path):
            rmtree(tempdir_path)
            mkdir(tempdir_path)
        return self

    def zip_mcpack_or_both(self, mergejavasky):
        if configs['settings'].get('export_zip'):
            path_zip = path.join(self.zippack_file(), "assets", "minecraft", "mcpatcher", "sky", "world0")
            super().make_pack_meta()
            self.make_pack_icon(self.old_names[3], self.zippack_file(), "pack.png")
            mergejavasky.save(path.join(tempdir, path_zip, 'cloud1.png'))
            for i in range(1, 9):
                if i != 5:
                    sky_properties = f"sky{i}.properties"
                    copy(path.join("resource", "mcpatcher", "sky", "world0", sky_properties),
                         path.join(tempdir, path_zip, sky_properties))
            self.move_to_out(self.zippack_file())

        if configs['settings'].get('export_mcpack'):
            path_mcpack = path.join(self.mcpack_file(), "textures", "environment", "overworld_cubemap")
            super().make_manifest()
            self.make_pack_icon(self.old_names[3], self.mcpack_file(), "pack_icon.png")
            for i in range(6):
                old_name = self.old_names[i]
                new_name = self.new_names[i]
                copy(path.join(tempdir, old_name), path.join(tempdir, path_mcpack, new_name))
            self.move_to_out(self.mcpack_file())

        if not configs['settings'].get('export_zip') and not configs['settings'].get('export_mcpack'):
            output_folder = path.join(configs['settings']['output_folder'], "MC-Sky-Builder", strftime("(%b-%d-%Y) %H-%M-%S"))
            if path.exists(output_folder):
                rmtree(output_folder)
            copytree(tempdir, output_folder)
        return self
