# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])


#os.system(f'cmd /c python crawler_map_data.py')
os.system(f'cmd /c python crawler_monsters.py')
os.system(f'cmd /c python crawler_resource.py')