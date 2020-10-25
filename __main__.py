# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

# Import system
from src.training.trainer import Trainer
from database.sqlite import Database

print('Initialize database module')
database = Database()
print('Initialize treiner module')
trainer = Trainer(database=database)

while True: 
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
     ____   ___  _____ _   _ ____    ____   ___ _____ 
    |  _ \ / _ \|  ___| | | / ___|  | __ ) / _ \_   _|
    | | | | | | | |_  | | | \___ \  |  _ \| | | || |  
    | |_| | |_| |  _| | |_| |___) | | |_) | |_| || |  
    |____/ \___/|_|    \___/|____/  |____/ \___/ |_|  
        By Lucas Sievers
    """
    )
    print('SELECT ONE OF THE OPTIONS')
    print('1  - Trainer')
    print('-1 - Exit')
    option = int(input("Select what you want: "))
    if option == 1:
        trainer.set_train_type('res')
        print(trainer.get_train_image_list())
        trainer.run(pos_list=[])
        database.connection.close()
        

    elif option == -1:
        break
