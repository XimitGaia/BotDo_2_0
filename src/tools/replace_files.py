#Autoloader
import os





class replace_files:

    
    
    @staticmethod
    def get_dofus_base_content_path():
        base_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}content"
        if os.path.exists(base_path):
            base_path = base_path
            print('Dofus content fold: OK')
        else:
            raise Exception("Dofus content folder not found!") 
