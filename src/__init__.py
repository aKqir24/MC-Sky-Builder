from os import path, mkdir
from .config import tempdir, config_folder, config_file, writeconfig, readconfig

class EnvironmentInitializer:
    if not path.exists(tempdir):
        mkdir(tempdir)
    if not path.exists(config_folder):
        mkdir(config_folder)

    def set_defaults(self):
        if not path.exists(config_file):
            writeconfig()
        readconfig()
        return self

EnvironmentInitializer().set_defaults()
