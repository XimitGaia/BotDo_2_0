#Autoloader
import os
import distutils
from distutils import dir_util


local_base_path = os.path.dirname(os.path.realpath(__file__))
local_path = f'{local_base_path}{os.sep}files_to_replace'
dofus_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}content{os.sep}themes"
distutils.dir_util.copy_tree(local_path,dofus_path)
