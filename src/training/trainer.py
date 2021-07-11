# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

# default imports
import time
from PIL import Image
import os
import PIL.ImageOps
from os import listdir
from tabulate import tabulate
import shutil
import re
import numpy as np

# Import system
from src.tools.search import Search
from database.sqlite import Database


class Trainer:
    def __init__(self, database):
        self.database: Database = database
        self.base_path = None
        self.get_dofus_base_content_path()
        self.screens_folder_path = f"{self.folder_base_path}{os.sep}Screens"
        self.output_folder_path = f"{self.folder_base_path}{os.sep}Output"
        self.temp_folder_path = f"{self.folder_base_path}{os.sep}Temp"

    def set_train_type(self, train_type: str):
        self.train_type = train_type

    def get_train_type(self) -> str:
        return self.train_type

    def get_train_image_list(self) -> list:
        images_map = {
            "res": [
                f"{os.sep}themes{os.sep}darkStone{os.sep}texture{os.sep}Characteristics{os.sep}tx_res_air.png",
                f"{os.sep}themes{os.sep}darkStone{os.sep}texture{os.sep}Characteristics{os.sep}tx_res_earth.png",
                f"{os.sep}themes{os.sep}darkStone{os.sep}texture{os.sep}Characteristics{os.sep}tx_res_fire.png",
                f"{os.sep}themes{os.sep}darkStone{os.sep}texture{os.sep}Characteristics{os.sep}tx_res_neutral.png",
                f"{os.sep}themes{os.sep}darkStone{os.sep}texture{os.sep}Characteristics{os.sep}tx_res_water.png",
            ]
        }
        list_to_return = list()
        for image_relative_path in images_map.get(self.get_train_type()):
            list_to_return.append(f"{self.base_path}{image_relative_path}")
        return list_to_return

    def get_dofus_base_content_path(self):
        base_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}content"
        self.folder_base_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(base_path):
            self.base_path = base_path
            print("Dofus content fold: OK")
        else:
            raise Exception("Dofus content folder not found!")

    def get_name_from_path(self, path):
        path_array = path.split(os.sep)
        return path_array[-1].split(".")[0]

    def filter_dir_list(self, dir_list: list):
        return [output_path for output_path in dir_list if output_path != ".gitkeep"]

    def run(
        self,
        pos_list: list,
        match_tolerance: tuple = (0.01, 0.13, 0.02),
        color_tolerance: tuple = (0.02, 0.12, 0.02),
        valid_group_porcentage: tuple = (0.02, 0.12, 0.02),
        saturation_tolerance: tuple = (0.02, 0.12, 0.02),
        bright_tolerance: tuple = (0.02, 0.12, 0.02),
    ):
        img_list = self.filter_dir_list(self.get_train_image_list())
        screen_list = self.filter_dir_list(os.listdir(self.screens_folder_path))
        pos_list = pos_list
        match_min, match_max, match_step = match_tolerance
        color_min, color_max, color_step = color_tolerance
        group_min, group_max, group_step = valid_group_porcentage
        saturation_min, saturation_max, saturation_step = saturation_tolerance
        bright_min, bright_max, bright_step = bright_tolerance
        for img in img_list:
            for scr in screen_list:
                print(f"Processing \nimg: {img}\n on scr: {scr}")
                image = Image.open(img)
                screen = Image.open(f"{self.screens_folder_path}{os.sep}{scr}")
                # image = image.resize((23,23),Image.ANTIALIAS) #tumbnail optional
                Table = []
                match_count = match_min
                for i in np.arange(match_min, match_max + 0.01, match_step):
                    color_count = color_min
                    for j in np.arange(
                        color_min, color_max + 0.01, color_step
                    ):  #!!!!!!!!!!!!!!!!! ajeitar step
                        group_count = group_min
                        for k in np.arange(group_min, group_max + 0.01, group_step):
                            saturation_count = saturation_min
                            for l in np.arange(
                                saturation_min, saturation_max + 0.01, saturation_step
                            ):
                                bright_count = bright_min
                                for m in np.arange(
                                    bright_min, bright_max + 0.01, bright_step
                                ):
                                    match_list, time_total = Search.search_image(
                                        image=image,
                                        screen=screen,
                                        match_tolerance=match_count,
                                        color_tolerance=color_count,
                                        validator_group_porcentage=group_count,
                                        saturation_tolerance=saturation_count,
                                        bright_tolerance=bright_count,
                                        trainer=True,
                                    )
                                    total_matches = len(set(pos_list) & set(match_list))
                                    total_miss_matches = len(match_list) - total_matches
                                    self.database.insert_training_results(
                                        row=(
                                            f"{self.get_name_from_path(img)}_{self.get_name_from_path(scr)}",
                                            round(match_count, 3),
                                            round(color_count, 3),
                                            round(group_count, 3),
                                            round(saturation_count, 3),
                                            round(bright_count, 3),
                                            total_matches,
                                            total_miss_matches,
                                            time_total,
                                        )
                                    )
                                    bright_count += bright_step
                                saturation_count += saturation_step
                            group_count += group_step
                        color_count += color_step
                    match_count += match_step


if __name__ == "__main__":
    print("Initialize database module")
    database = Database()
    t = Trainer(database=database)
    t.set_train_type("res")
    print(t.get_train_image_list())
    t.run(pos_list=[])
