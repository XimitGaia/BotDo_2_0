#Autoloader
import os
import distutils
from distutils import dir_util

def replace_files():
    local_base_path = os.path.dirname(os.path.realpath(__file__))
    local_path = f'{local_base_path}{os.sep}files_to_replace'
    dofus_theme_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus"
    ui_positions_log = f"{os.getenv('APPDATA')}{os.sep}Dofus{os.sep}Berilia_ui_positions.dat"

    distutils.dir_util.copy_tree(local_path,dofus_theme_path)
    if os.path.exists(ui_positions_log):
        os.remove(ui_positions_log)