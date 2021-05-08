# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(f'{root_path}{os.sep}database{os.sep}dofus_sqlite.db')
        self.check_or_create_tables()
        self.insert_values()

    def __del__(self):
        self.connection.close()
    #
    #       ::::::::  :::    ::: :::::::::: ::::::::  :::    :::            ::::::::  :::::::::             ::::::::  :::::::::  ::::::::::     ::: ::::::::::: ::::::::::
    #     :+:    :+: :+:    :+: :+:       :+:    :+: :+:   :+:            :+:    :+: :+:    :+:           :+:    :+: :+:    :+: :+:          :+: :+:   :+:     :+:
    #    +:+        +:+    +:+ +:+       +:+        +:+  +:+             +:+    +:+ +:+    +:+           +:+        +:+    +:+ +:+         +:+   +:+  +:+     +:+
    #   +#+        +#++:++#++ +#++:++#  +#+        +#++:++              +#+    +:+ +#++:++#:            +#+        +#++:++#:  +#++:++#   +#++:++#++: +#+     +#++:++#
    #  +#+        +#+    +#+ +#+       +#+        +#+  +#+             +#+    +#+ +#+    +#+           +#+        +#+    +#+ +#+        +#+     +#+ +#+     +#+
    # #+#    #+# #+#    #+# #+#       #+#    #+# #+#   #+#            #+#    #+# #+#    #+#           #+#    #+# #+#    #+# #+#        #+#     #+# #+#     #+#
    # ########  ###    ### ########## ########  ###    ### ########## ########  ###    ### ########## ########  ###    ### ########## ###     ### ###     ##########
    #

    def check_if_tabel_exists(self, table_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';""")
        results = cursor.fetchall()
        cursor.close()
        for row in results:
            if row[0] == table_name:
                return True
        return False

    def check_or_create_tables(self):
        cursor = self.connection.cursor()
        tables = {
            'job_type':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        job_type TEXT UNIQUE
                    );
                """,
                'with_index': False
            },
            'jobs':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        job_name TEXT UNIQUE,
                        job_type integer,
                        FOREIGN KEY(job_type) REFERENCES job_type(id)
                    );
                """,
                'with_index': False
            },
            'harvestables_list':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        resources_name TEXT UNIQUE,
                        resources_level integer,
                        job_id integer,
                        images_id integer,
                        FOREIGN KEY(job_id) REFERENCES jobs(id)
                        FOREIGN KEY(images_id) REFERENCES images(id)
                    );
                """,
                'with_index': False
            },
            'monsters': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        monster_id INTEGER,
                        monster_name TEXT,
                        monster_type TEXT,
                        level INTEGER,
                        life_points INTEGER,
                        action_points INTEGER,
                        movement_points INTEGER,
                        pa_dodge INTEGER,
                        pm_dodge INTEGER,
                        earth_resistance INTEGER,
                        air_resistance INTEGER,
                        fire_resistance  INTEGER,
                        water_resistance INTEGER,
                        neutral_resistance INTEGER,
                        can_trackle INTEGER,
                        can_be_pushed INTEGER,
                        can_switch_pos INTEGER,
                        can_switch_pos_on_target INTEGER,
                        can_be_carried INTEGER
                    );
                """,
                'with_index': False
            },
            'drops': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        item_id integer PRIMARY KEY,
                        item_name TEXT,
                        item_level INTEGER,
                        monster_id INTEGER,
                        drop_rate REAL,
                        FOREIGN KEY(monster_id) REFERENCES monsters(id)
                    );
                """,
                'with_index': False
            },
            'world_map': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY,
                        x INTEGER,
                        y INTEGER,
                        top INTEGER,
                        left INTEGER,
                        bottom INTEGER,
                        right INTEGER,
                        outdoors INTEGER,
                        sub_area_id INTEGER,
                        area_id INTEGER,
                        verified TEXT
                    );
                """,
                'with_index': False
            },
            'surface_sub_areas': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        sub_area_id integer PRIMARY KEY,
                        sub_area_name TEXT
                    );
                """,
                'with_index': False
            },
            'interactives': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        world_map_id INTEGER,
                        element_id INTEGER,
                        type TEXT,
                        cell_id INTEGER,
                        off_set_x INTEGER,
                        off_set_y INTEGER,
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                'with_index': False
            },
            'monsters_location': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        world_map_id INTEGER,
                        monster_id INTEGER REFERENCES monsters(monster_id),
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                'with_index': False
            },
            'connections': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        destiny INTEGER,
                        interactive_id INTEGER,
                        FOREIGN KEY(interactive_id) REFERENCES interactives(id),
                        FOREIGN KEY(destiny) REFERENCES world_map(id)
                    );
                """,
                'with_index': False
            },
            'zaaps': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        name TEXT UNIQUE,
                        world_map_id INTEGER,
                        x INTEGER,
                        y INTEGER,
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                'with_index': False
            },
            'harvestables_cells': {
                'temp': False,
                'sql': """
                    CREATE TABLE *table*(
                        harvestable_id INTEGER,
                        interactive_id INTEGER,
                        FOREIGN KEY(interactive_id) REFERENCES interactives(id),
                        FOREIGN KEY(harvestable_id) REFERENCES harvestables_list(id)
                    );
                """,
                'with_index': False
            },
        }
        for table in tables:
            tables_to_create = [table]
            if tables[table]['temp']:
                tables_to_create.append(f"{table}_temp")
            sql = tables[table]['sql']
            for table_to_create in tables_to_create:
                if not self.check_if_tabel_exists(table_to_create):
                    create_table = sql.replace('*table*', table_to_create)
                    cursor.execute(create_table)
                    if tables[table]['with_index']:
                        index = f"""
                            CREATE UNIQUE INDEX IF NOT EXISTS {table_to_create}_id_index
                            ON {table_to_create}(ID);
                        """
                        cursor.execute(index)
                    self.connection.commit()
        cursor.close()

    #       ::::::::::: ::::    :::  ::::::::  :::::::::: ::::::::: ::::::::::: ::::::::
    #          :+:     :+:+:   :+: :+:    :+: :+:        :+:    :+:    :+:    :+:    :+:
    #         +:+     :+:+:+  +:+ +:+        +:+        +:+    +:+    +:+    +:+
    #        +#+     +#+ +:+ +#+ +#++:++#++ +#++:++#   +#++:++#:     +#+    +#++:++#++
    #       +#+     +#+  +#+#+#        +#+ +#+        +#+    +#+    +#+           +#+
    #      #+#     #+#   #+#+# #+#    #+# #+#        #+#    #+#    #+#    #+#    #+#
    # ########### ###    ####  ########  ########## ###    ###    ###     ########

    def insert_job_type(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO job_type(job_type) VALUES (?);""", row)
        self.connection.commit()

    def insert_jobs(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO jobs(job_name, job_type) VALUES (?, ?);""", row)
        self.connection.commit()

    def insert_harvestables_list(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO harvestables_list(resources_name, resources_level, job_id, images_id) VALUES (?, ?, ?, ?);""", row)
        self.connection.commit()

    def insert_monsters(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO monsters(monster_id, monster_name, monster_type, level, life_points, action_points, movement_points, pa_dodge, pm_dodge, earth_resistance, air_resistance, fire_resistance , water_resistance, neutral_resistance, can_trackle, can_be_pushed, can_switch_pos, can_switch_pos_on_target, can_be_carried) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", row)
        self.connection.commit()

    def insert_world_map(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO world_map(id, x, y,top, left, bottom, right, outdoors, sub_area_id, area_id, verified) values(?,?,?,?,?,?,?,?,?,?,?);""", row)
        self.connection.commit()
        return cursor.lastrowid

    def insert_zaaps(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO zaaps(name, world_map_id, x, y) values(?,?,?,?);""", row)
        self.connection.commit()

    def insert_harvestables_cells(self, harvestable_id, element_id):
        cursor = self.connection.cursor()
        cursor.execute(
            f"""
                INSERT OR IGNORE INTO harvestables_cells(harvestable_id, interactive_id)
                SELECT {harvestable_id} as harvestable_id, id
                FROM interactives
                WHERE element_id = {element_id}
            """
        )
        self.connection.commit()

    def insert_drops(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO drops(item_id, item_name, item_level, monster_id, drop_rate) values(?,?,?,?,?);""", row)
        self.connection.commit()

    def insert_interactives(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO interactives(world_map_id, element_id, type, cell_id, off_set_x, off_set_y) values(?,?,?,?,?,?);""", row)
        self.connection.commit()

    def insert_surface_sub_areas(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO surface_sub_areas(sub_area_id, sub_area_name) values(?,?);""", row)
        self.connection.commit()

    def insert_monster_location(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO monsters_location(world_map_id, monster_id) values(?,?);""", row)
        self.connection.commit()

    def insert_connector(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO connections(destiny, interactive_id) values(?,?);""", row)
        self.connection.commit()

    # :::    ::: :::::::::  :::::::::      ::: ::::::::::: ::::::::::
    # :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:     :+:
    # +:+    +:+ +:+    +:+ +:+    +:+  +:+   +:+  +:+     +:+
    # +#+    +:+ +#++:++#+  +#+    +:+ +#++:++#++: +#+     +#++:++#
    # +#+    +#+ +#+        +#+    +#+ +#+     +#+ +#+     +#+
    # #+#    #+# #+#        #+#    #+# #+#     #+# #+#     #+#
    #  ########  ###        #########  ###     ### ###     ##########

    def update_world_map(self, row: tuple, column_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"""UPDATE  world_map set {column_name} = ? where id = ?;""", row)
        self.connection.commit()

    #   :+:     :+:   :+: :+:   :+:       :+:    :+: :+:       :+:    :+:
    #  +:+     +:+  +:+   +:+  +:+       +:+    +:+ +:+       +:+
    # +#+     +:+ +#++:++#++: +#+       +#+    +:+ +#++:++#  +#++:++#++
    # +#+   +#+  +#+     +#+ +#+       +#+    +#+ +#+              +#+
    # #+#+#+#   #+#     #+# #+#       #+#    #+# #+#       #+#    #+#
    #  ###     ###     ### ########## ########  ########## ########

    def insert_values(self):
        self.insert_values_job_type_2020_11_02()
        self.insert_values_jobs_2020_11_02()
        self.insert_value_harvestables_2021_05_02()
        self.insert_values_surface_sub_areas_2021_03_05()

    def insert_values_executor(self, callback, values_list: list):
        for values in values_list:
            callback(values)

    def insert_values_job_type_2020_11_02(self):
        values_list =[
            ('drop_collecting',),
            ('collecting',),
        ]
        self.insert_values_executor(callback=self.insert_job_type, values_list=values_list)

    def insert_values_jobs_2020_11_02(self):
        values_list =[
            ('lumberjack', 2),
            ('farmer', 2),
            ('alchemist', 2),
            ('miner', 2),
            ('fishman', 2),
            ('Artificer', 1),
            ('Carver', 1),
            ('Handyman', 1),
            ('Jeweller', 1),
            ('Shoemaker ', 1),
            ('Smith', 1),
            ('Tailor', 1),

        ]
        self.insert_values_executor(callback=self.insert_jobs, values_list=values_list)

    def insert_value_harvestables_2021_05_02(self):
        values_list =[
            ('Ash', 1, 1, 1),
            ('Chestnut', 20, 1, 1),
            ('Walnut', 40, 1, 1),
            ('Oak', 60, 1, 1),
            ('Bombu', 70, 1, 1),
            ('Maple', 80, 1, 1),
            ('Oliviolet', 90, 1, 1),
            ('Yew', 100, 1, 1),
            ('Bamboo', 110, 1, 1),
            ('Cherry', 120, 1, 1),
            ('Hazel', 130, 1, 1),
            ('Ebony', 140, 1, 1),
            ('Kaliptus', 150, 1, 1),
            ('Hornbeam', 160, 1, 1),
            ('Dark Bamboo', 170, 1, 1),
            ('Elm', 180, 1, 1),
            ('Holy Bamboo', 190, 1, 1),
            ('Aspen', 200, 1, 1),
            ('Mahaquany', 200, 1, 1),
            ('Wheat', 1, 2, 1),
            ('Barley', 20, 2, 1),
            ('Oats', 40, 2, 1),
            ('Hop Hop', 60, 2, 1),
            ('Flax', 80, 2, 1),
            ('Rice', 100, 2, 1),
            ('Rye Rye', 100, 2, 1),
            ('Malt', 120, 2, 1),
            ('Hemp', 140, 2, 1),
            ('Corn', 160, 2, 1),
            ('Millet', 180, 2, 1),
            ('Frosteez', 200, 2, 1),
            ('Quisnoa', 200, 2, 1),
            ('Nettles', 1, 3, 1),
            ('Sage', 20, 3, 1),
            ('Five-Leaf Clover', 40, 3, 1),
            ('Wild Mint', 60, 3, 1),
            ('Freyesque Orchid', 80, 3, 1),
            ('Edelweiss', 100, 3, 1),
            ('Pandkin Seed', 120, 3, 1),
            ('Ginseng', 140, 3, 1),
            ('Belladonna', 160, 3, 1),
            ('Mandrake', 180, 3, 1),
            ('Salikronia', 200, 3, 1),
            ('Snowdrop', 200, 3, 1),
            ('Iron', 10, 4, 1),
            ('Copper', 20, 4, 1),
            ('Bronze', 40, 4, 1),
            ('Cobalt', 60, 4, 1),
            ('Manganese', 80, 4, 1),
            ('Tin', 100, 4, 1),
            ('Silicate', 100, 4, 1),
            ('Silver', 120, 4, 1),
            ('Bauxite', 140, 4, 1),
            ('Gold', 160, 4, 1),
            ('Dolomite', 180, 4, 1),
            ('Obsidian', 200, 4, 1),
            ('Sepiolite', 200, 4, 1),
            ('Gudgeon', 1, 5, 1),
            ('Grawn', 10, 5, 1),
            ('Trout', 20, 5, 1),
            ('Crab Surimi', 30, 5, 1),
            ('Kittenfish', 40, 5, 1),
            ('Breaded Fish', 50, 5, 1),
            ('Ediem Carp', 60, 5, 1),
            ('Shiny Sardine', 70, 5, 1),
            ('Pike', 80, 5, 1),
            ('Kralove', 90, 5, 1),
            ('Eel', 100, 5, 1),
            ('Grey Sea Bream', 110, 5, 1),
            ('Perch', 120, 5, 1),
            ('Blue Ray', 130, 5, 1),
            ('Monkfish', 140, 5, 1),
            ('Sickle-Hammerhead Shark', 150, 5, 1),
            ('Lard Bass', 160, 5, 1),
            ('Cod', 170, 5, 1),
            ('Tench', 180, 5, 1),
            ('Swordfish', 190, 5, 1),
            ('Icefish', 200, 5, 1),
            ('Limpet', 200, 5, 1),
        ]
        self.insert_values_executor(callback=self.insert_harvestables_list, values_list=values_list)

    def insert_values_zaaps_2021_05_05(self):
        values_list = [
            ("Amakna Castle", 68552706, 3, -5),
            ("Amakna Village", 88213271, -2, 0),
            ("Crackler Mountain", 185860609, -5, -8),
            ("Edge of the Evil Forest", 88212746, -1, 13),
            ("Gobball Corner", 88082704, 5, 7),
            ("Madrestam Harbour", 68419587, 7, -4),
            ("Scaraleaf Plain", 88212481, -1, 24),
            ("Crocuzko", 197920772, -83, -15),
            ("Astrub City", 191105026, 5, -18),
            ("Bonta", 147768, -32, -56),
            ("Brakmar", 144419, -26, 35),
            ("Cania Lake", 156240386, -3, -42),
            ("Cania Massif", 165152263, -13, -28),
            ("Imp Village", 14419207, -16, -24),
            ("Kanig Village", 126094107, 0, -56),
            ("Lousy Pig Plain", 84806401, -5, -23),
            ("Rocky Plains", 147590153, -17, -47),
            ("Rocky Roads", 164364304, -20, -20),
            ("The Cania Fields", 142087694, -27, -36),
            ("Arch of Vili", 202899464, 15, -20),
            ("Dopple Village", 100270593, -34, -8),
            ("Entrance to Harebourg's Castle", 108789760, -67, -75),
            ("Frigost Village", 54172969, -78, -41),
            ("The Snowbound Village", 54173001, -77, -73),
            ("Breeder Village", 73400320, -16, 1),
            ("Turtle Beach", 156762120, 35, 12),
            ("Dunes of Bones", 173278210, 15, -58),
            ("Canopy Village", 20973313, -54, 16),
            ("Coastal Village", 154642, -46, 18),
            ("Pandala Village", 207619076, 20, -29),
            ("Caravan Alley", 171967506, -25, 12),
            ("Desecrated Highlands", 179831296, -15, 25),
            ("Alliance Temple", 115083777, 13, 35),
            ("Sufokia", 95422468, 13, 26),
            ("Sufokian Shoreline", 88085249, 10, 22),
            ("The Cradle", 120062979, 1, -32),
            ("Abandoned Labowatowies", 115737095, 27, -14),
            ("Cawwot Island", 99615238, 25, -4),
            ("Zoth Village", 28050436, -53, 18),
            ("Way of Souls", 154010371, -1, -3)
        ]
        self.insert_values_executor(callback=self.insert_zaaps, values_list=values_list)

    def insert_values_surface_sub_areas_2021_03_05(self):
        values_list = [
            (1, "Madrestam Harbour"),
            (2, "Crackler Mountain"),
            (3, "Ingalsses' Fields"),
            (4, "Amakna Forest"),
            (5, "Gobball Corner"),
            (6, "Cemetery"),
            (7, "Cemetery Crypts"),
            (8, "The Bwork Camp"),
            (9, "Evil Forest"),
            (10, "Amakna Village"),
            (11, "Porco Territory"),
            (12, "Jelly Peninsula"),
            (22, "Edge of the Evil Forest"),
            (23, "Dreggon Peninsula"),
            (27, "Asse Coast"),
            (30, "Tainela"),
            (31, "Amakna Swamps"),
            (32, "Sufokia"),
            (33, "Arak-hai Forest"),
            (43, "Bonta City Walls"),
            (44, "Bakers' Quarter"),
            (46, "Butchers' Quarter"),
            (47, "Smiths' Quarter"),
            (48, "Lumberjacks' Quarter"),
            (49, "Handymen's Quarter"),
            (50, "Tailors' Quarter"),
            (51, "Jewellers' Quarter"),
            (54, "Cania Massif"),
            (55, "The Crow's Domain"),
            (56, "Cania Lake"),
            (57, "Desolation of Sidimote"),
            (59, "Heroes' Cemetery"),
            (61, "Cemetery of the Tortured"),
            (62, "Dopple Village"),
            (68, "Cania Fields"),
            (69, "Eltneg Wood"),
            (70, "Rocky Plains"),
            (71, "Gisgoul"),
            (76, "Imp Village"),
            (84, "Trool Fair"),
            (93, "Turtle Beach"),
            (95, "Astrub City"),
            (96, "Astrub Quarry"),
            (97, "Astrub Forest"),
            (98, "Astrub Fields"),
            (102, "Astrub Cemetery"),
            (103, "Bandit Territory"),
            (161, "Cawwot Island"),
            (162, "Gwimace Island"),
            (163, "Gwavestone Island"),
            (164, "Isle of the Cwown"),
            (165, "The Forbidden Jungle"),
            (166, "The Forest of Masks"),
            (167, "Skull Path"),
            (168, "Dark Forest"),
            (169, "Edge of the Treechnid Forest"),
            (170, "Scaraleaf Plain"),
            (173, "Astrub Meadow"),
            (178, "Lousy Pig Plain"),
            (179, "Mushd Corner"),
            (180, "Amakna Castle"),
            (182, "Breeder Village"),
            (209, "Minotoror Island"),
            (230, "Primitive Cemetery"),
            (231, "Enchanted Lakes"),
            (232, "Nauseating Swamps"),
            (233, "Bottomless Swamps"),
            (234, "Kaliptus Forest"),
            (235, "Wild Dragoturkey Territory"),
            (253, "Wild Canyon"),
            (275, "Agony V'Helley"),
            (276, "The Goblin Camp"),
            (277, "Bwork Village"),
            (279, "Bonta Pasture"),
            (280, "Brakmar City Walls"),
            (315, "Dreggon Village"),
            (320, "Kwismas Haven"),
            (325, "Crocabulia's Lair"),
            (334, "Cania Bay"),
            (335, "Astrub Rocky Inlet"),
            (451, "Castaway Island"),
            (453, "Coral Beach"),
            (454, "Grassy Plains"),
            (455, "Dark Jungle"),
            (457, "Bottomless Peat Bog"),
            (464, "Tree Keeholo Trunk"),
            (465, "Breeder Village"),
            (466, "Coastal Village"),
            (471, "Putrid Peat Bog"),
            (472, "Tree Keeholo Foliage"),
            (479, "Kawaii River"),
            (480, "Low Crackler Mountain"),
            (481, "Brouce Boulgoure's Clearing"),
            (482, "Milicluster"),
            (485, "Amakna Countryside"),
            (490, "Sufokian Shoreline"),
            (492, "Passage to Brakmar"),
            (493, "Blop Fields"),
            (501, "Isle O'Anstitch"),
            (502, "Lumberjacks' Quarter"),
            (503, "Butchers' Quarter"),
            (505, "Bakers' Quarter"),
            (506, "Jewellers' Quarter"),
            (507, "Tailors' Quarter"),
            (508, "Smiths' Quarter"),
            (509, "Handymen's Quarter"),
            (511, "City Centre"),
            (513, "City Centre"),
            (517, "Desecrated Highlands"),
            (518, "Cania Moors"),
            (519, "Stontusk Desert"),
            (521, "Cania Peaks"),
            (522, "Howling Heights"),
            (523, "Cania Cirque"),
            (525, "Rocky Roads"),
            (526, "Caravan Alley"),
            (530, "Alchemists' Quarter"),
            (531, "Alchemists' Quarter"),
            (532, "Fishermen's Quarter"),
            (533, "Breeders' Quarter"),
            (534, "Fishermen's Quarter"),
            (535, "Breeders' Quarter"),
            (600, "Permafrost Port"),
            (601, "Frigost Village"),
            (602, "Icefields"),
            (603, "Snowbound Village"),
            (604, "Lonesome Pine Trails"),
            (605, "Petrified Forest"),
            (606, "Asparah Gorge"),
            (608, "Fangs of Glass"),
            (609, "Alma's Cradle"),
            (610, "Tears of Ouronigride"),
            (611, "Mount Scauldron"),
            (615, "Frozen Lake"),
            (650, "Sakai Harbour"),
            (651, "Sakai Plain"),
            (652, "Snowy Forest"),
            (757, "Kwismas Land"),
            (758, "Kwismas Taiga"),
            (762, "Vulkania Village"),
            (763, "Traktopel Forest"),
            (764, "Spartania Forest"),
            (765, "Stratigra Forest"),
            (772, "Vulkania"),
            (797, "Alliance Temple"),
            (798, "Abandoned Labowatowies"),
            (799, "Krismahlo Island"),
            (809, "Kanig Village"),
            (817, "Abandoned Halls"),
            (834, "Albatrocious Rock"),
            (848, "Mysterious Island"),
            (849, "Stone of the Sacrificed"),
            (850, "Kramdam Heights"),
            (872, "Dunes of Bones"),
            (873, "Castuc Territory"),
            (874, "Sarakech Port"),
            (878, "Gorge of Howling Winds"),
            (879, "Forgotten City"),
            (883, "Nimaltopia"),
            (886, "Brakmar Stud Farm"),
            (887, "Labyrinth of Deleterious Winds"),
            (889, "Fungus Domain"),
            (891, "Volcano Forge"),
            (896, "Magmatic Steps"),
            (902, "Kingdom of Freezammer"),
            (941, "Akwadala"),
            (942, "Plantala"),
            (943, "Feudala"),
            (944, "Terrdala"),
            (945, "Aerdala"),
            (951, "Pandala Village"),
            (952, "Nolifis Cemetery"),
            (955, "Mount Tombs"),
            (960, "Forbidden Inn")
        ]
        self.insert_values_executor(callback=self.insert_surface_sub_areas, values_list=values_list)

    # def create_resources_location_view(self):

#        ::::::::   :::    ::: :::::::::: :::    ::: :::::::::: ::::::::
#      :+:    :+:  :+:    :+: :+:        :+:    :+: :+:       :+:    :+:
#     +:+    +:+  +:+    +:+ +:+        +:+    +:+ +:+       +:+
#    +#+    +:+  +#+    +:+ +#++:++#   +#+    +:+ +#++:++#  +#++:++#++
#   +#+    +#+  +#+    +#+ +#+        +#+    +#+ +#+              +#+
#  #+#    #+#  #+#    #+# #+#        #+#    #+# #+#       #+#    #+#
#  ########### ########  ##########  ########  ########## ########

    def query(self, sql: str):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def get_resource_by_name_or_id(self, name_or_id) -> dict:
        sql = ""
        if name_or_id.isdigit():
            sql = f"""
                SELECT * FROM harvestables_list
                WHERE id = {name_or_id}
            """
        elif type(name_or_id) is str:
            sql = f"""
                SELECT * FROM harvestables_list
                WHERE resources_name like '%{name_or_id}%'
            """
        if sql == '':
            return {}
        return self.query(sql)

    def get_jobs(self):
        sql = """
            SELECT * FROM jobs
        """
        return self.query(sql)

    def get_resources_by_job_id(self, job_id):
        sql = f"""
            SELECT * FROM harvestables_list
            WHERE job_id = {job_id}
        """
        return self.query(sql)

    def get_resources_location(self, job_resources_id_list: list):
        id_list_sql = ", ".join(job_resources_id_list)
        sql = f"""
            SELECT * FROM job_resources_location
            WHERE resources_id in  ({id_list_sql})
        """
        return self.query(sql)

    def get_primary_neighborhood(self, world_map_id):
        sql = f"""
                SELECT wp.top, wp.left, wp.right, wp.bottom FROM world_map wp
                WHERE id = {world_map_id};
        """
        return self.query(sql)

    def get_connectors(self, world_map_id: int):
        sql = f"""
            SELECT conn.destiny, conn.interactive_id FROM connections conn
            JOIN interactives inter ON inter.id = conn.interactive_id
            WHERE inter.world_map_id = {world_map_id}
        """
        return self.query(sql)

    def get_unknown_interactives_position(self, world_map_id: int):
        sql = f"""
            SELECT inter.cell_id, off_set_x, off_set_y FROM interactives inter
            WHERE world_map_id = {world_map_id}
            AND (type = "connector" OR type == "unknown")
            AND inter.id NOT IN (SELECT interactive_id FROM connections)
        """
        return self.query(sql)

    def get_zaaps(self):
        sql = """
            SELECT * FROM zaaps
        """
        return self.query(sql)

    def get_map_id(self, pos: tuple, world_list_zone: int):
        sql = f"""
            SELECT id FROM world_map
            WHERE x = {pos[0]} and
            y = {pos[1]} and
            world_list_zone = {world_list_zone}
        """
        return self.query(sql)

    # terminar
    def get_harvestables_cells_by_map_id(self, harvestables: list, map_id: int):
        harvestables = [str(i.get('id')) for i in harvestables]
        sql = f"""
            SELECT hc.cell_number FROM harvestables_cells hc
            WHERE world_map_id = {map_id} AND
            item_id in ({', '.join(harvestables)})
        """
        return self.query(sql)

    def get_harvestables_cells_by_pos_and_world_zone(self, harvestables: list, pos: tuple):
        harvestables = [str(i.get('id')) for i in harvestables]
        select = ', '.join(harvestables)
        sql = f"""
            SELECT
            hc.cell_number
            FROM world_map wp
            LEFT JOIN harvestables_cells hc on wp.id = hc.world_map_id
            LEFT JOIN harvestables_list jr on hc.item_id = jr.id
            WHERE
            x={pos[0]} and
            y={pos[1]} AND
            world_list_zone_id = {pos[2]} AND
            hc.item_id in ({select});
        """
        return self.query(sql)

    def get_main_world_map_sub_areas(self):
        sql =   """
            SELECT sub_area_id
            FROM surface_sub_areas
        """
        return self.query(sql)

# :::     ::: ::::::::::: :::::::::: :::       :::
# :+:     :+:     :+:     :+:        :+:       :+:
# +:+     +:+     +:+     +:+        +:+       +:+
# +#+     +:+     +#+     +#++:++#   +#+  +:+  +#+
#  +#+   +#+      +#+     +#+        +#+ +#+#+ +#+
#   #+#+#+#       #+#     #+#         #+#+# #+#+#
#     ###     ########### ##########   ###   ###

    def create_harvestables_location_view(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
                CREATE VIEW harvestables_location AS
                SELECT inter.world_map_id, harvest.harvestable_id, count(*) as "quantity" FROM interactives inter JOIN harvestables_cells harvest
                ON inter.id = harvest.interactive_id
                WHERE type = "harvestable"
                GROUP BY world_map_id,harvestable_id
            """
        )
        self.connection.commit()


# if __name__ == '__main__':
#     database = Database()
#     print(database.get_connectors(5506052))
