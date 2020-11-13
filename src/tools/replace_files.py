#Autoloader
import os
import distutils
from distutils import dir_util

def replace_files():
    local_base_path = os.path.dirname(os.path.realpath(__file__))
    local_path_local = f'{local_base_path}{os.sep}files_to_replace{os.sep}local'
    local_path_roaming = f'{local_base_path}{os.sep}files_to_replace{os.sep}roaming'
    dofus_local_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus"
    dofus_roaming_path = f"{os.getenv('APPDATA')}"
    distutils.dir_util.copy_tree(local_path_local,dofus_local_path)
    distutils.dir_util.copy_tree(local_path_roaming,dofus_roaming_path)

if __name__ == "__main__":
    replace_files()