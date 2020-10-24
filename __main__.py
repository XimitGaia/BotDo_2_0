# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

# Import system
from src.training.trainer import Trainer



t = Trainer()
t.set_train_type('res')
print(t.get_train_image_list())