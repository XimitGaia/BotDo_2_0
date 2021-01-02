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
            'world_list_zone':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        zone_name TEXT UNIQUE
                    );
                """,
                'with_index': False
            },
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
            'images':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        path_from_root TEXT UNIQUE
                    );
                """,
                'with_index': False
            },
            'job_resources_list':  {
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
            'job_resources_location':  {
                'temp': False,
                'sql':  """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        x INTEGER,
                        y INTEGER,
                        resources_id,
                        resources_quantity integer,
                        world_list_zone_id integer,
                        FOREIGN KEY(resources_id) REFERENCES job_resources_list(id)
                        FOREIGN KEY(world_list_zone_id) REFERENCES world_list_zone(id)
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
                    level INTEGER,
                    lifePoints INTEGER,
                    actionPoints INTEGER,
                    movementPoints INTEGER,
                    earthResistance INTEGER,
                    airResistance INTEGER,
                    fireResistance  INTEGER,
                    waterResistance INTEGER,
                    neutralResistance INTEGER
                )
                """,
                'with_index': False
            },
            'barrers': {
                'temp': False,
                'sql': """
                CREATE TABLE *table*(
                    x INTEGER,
                    y INTEGER,
                    top INTEGER,
                    left INTEGER,
                    down INTEGER,
                    right INTEGER,
                    world_list_zone_id INTEGER
                )
                """,
                'with_index': False
            },
            'zaaps': {
                'temp': False,
                'sql': """
                CREATE TABLE *table*(
                    name TEXT UNIQUE,
                    x INTEGER,
                    y INTEGER
                )
                """,
                'with_index': False
            }
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


    def insert_world_list_zone(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""insert OR IGNORE into world_list_zone(zone_name) values(?);""", row)
        self.connection.commit()

    def insert_job_type(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO job_type(job_type) VALUES (?);""", row)
        self.connection.commit()

    def insert_jobs(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO jobs(job_name, job_type) VALUES (?, ?);""" , row)
        self.connection.commit()

    def insert_images(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""insert OR IGNORE into images(path_from_root) values(?);""" , row)
        self.connection.commit()

    def insert_job_resources_list(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT OR IGNORE INTO job_resources_list(resources_name, resources_level, job_id, images_id) VALUES (?, ?, ?, ?);""", row)
        self.connection.commit()

    def insert_job_resources_location(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute("""insert OR IGNORE into job_resources_location (x, y, resources_id, resources_quantity, world_list_zone_id) values(?, ?, ?, ?, ?);""" , row)
        self.connection.commit()

    def insert_monsters(self, row: tuple):
        cursosr = self.connection.cursor()
        cursosr.execute("""INSERT OR IGNORE INTO monsters(monster_id,monster_name,level, lifePoints, actionPoints, movementPoints, earthResistance, airResistance, fireResistance , waterResistance, neutralResistance) values(?,?,?,?,?,?,?,?,?,?,?);""",row)
        self.connection.commit()

    def insert_barrers(self, row: tuple):
        cursosr = self.connection.cursor()
        cursosr.execute("""INSERT OR IGNORE INTO barrers(x,y,top, left, down, right, world_list_zone_id) values(?,?,?,?,?,?,?);""",row)
        self.connection.commit()

    def insert_zaaps(self, row: tuple):
        cursosr = self.connection.cursor()
        cursosr.execute("""INSERT OR IGNORE INTO zaaps(name, x, y) values(?,?,?);""",row)
        self.connection.commit()


    #   :+:     :+:   :+: :+:   :+:       :+:    :+: :+:       :+:    :+:
    #  +:+     +:+  +:+   +:+  +:+       +:+    +:+ +:+       +:+
    # +#+     +:+ +#++:++#++: +#+       +#+    +:+ +#++:++#  +#++:++#++
    # +#+   +#+  +#+     +#+ +#+       +#+    +#+ +#+              +#+
    # #+#+#+#   #+#     #+# #+#       #+#    #+# #+#       #+#    #+#
    #  ###     ###     ### ########## ########  ########## ########

    def insert_values(self):
        self.insert_values_world_list_2020_11_02()
        self.insert_values_job_type_2020_11_02()
        self.insert_values_jobs_2020_11_02()
        self.insert_values_images_2020_11_02()
        self.insert_value_resources_20_11_02()
        self.insert_values_zaaps_2021_01_01()

    def insert_values_executor(self, callback, values_list: list):
        for values in values_list:
            callback(values)

    def insert_values_world_list_2020_11_02(self):
        values_list =[
            ('continent_amaknien',)
        ]
        self.insert_values_executor(callback=self.insert_world_list_zone, values_list=values_list)

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

    def insert_values_images_2020_11_02(self):
        values_list =[
            ('dummy',),
        ]
        self.insert_values_executor(callback=self.insert_images, values_list=values_list)

    def insert_value_resources_20_11_02(self):
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
        self.insert_values_executor(callback=self.insert_job_resources_list, values_list=values_list)

    def insert_values_zaaps_2021_01_01(self):
        values_list = [
            ("Amakna Castle", 3, -5),
            ("Amakna Village", -2, 0),
            ("Crackler Mountain", -5, -8),
            ("Edge of the Evil Forest", -1, 13),
            ("Gobball Corner", 5, 7),
            ("Madrestam Harbour", 7, -4),
            ("Scaraleaf Plain", -1, 24),
            ("Crocuzko", -83, -15),
            ("Astrub City", 5, -18),
            ("Bonta", -32, -56),
            ("Brakmar", -26, 35),
            ("Cania Lake", -3, -42),
            ("Cania Massif", -13, -28),
            ("Imp Village", -16, -24),
            ("Kanig Village", 0, -56),
            ("Lousy Pig Plain", -5, -23),
            ("Rocky Plains", -17, -47),
            ("Rocky Roads", -20, -20),
            ("The Cania Fields", -27, -36),
            ("Arch of Vili", 15, -20),
            ("Dopple Village", -34, -8),
            ("Entrance to Harebourg's Castle", -67, -75),
            ("Frigost Village", -78, -41),
            ("The Snowbound Village", -77, -73),
            ("Breeder Village", -16, 1),
            ("Turtle Beach", 35, 12),
            ("Dunes of Bones", 15, -58),
            ("Canopy Village", -54, 16),
            ("Coastal Village", -46, 18),
            ("Pandala Village", 20, -29),
            ("Caravan Alley", -25, 12),
            ("Desecrated Highlands", -15, 25),
            ("Alliance Temple", 13, 35),
            ("Sufokia", 13, 26),
            ("Sufokian Shoreline", 10, 22),
            ("The Cradle", 1, -32),
            ("Abandoned Labowatowies", 27, -14),
            ("Cawwot Island", 25, -4),
            ("Zoth Village", -53, 18)
        ]
        self.insert_values_executor(callback=self.insert_zaaps, values_list=values_list)




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

    def get_resource_by_name_or_id(self, name_or_id)-> dict:
        sql = ""
        if name_or_id.isdigit():
            sql = f"""
                SELECT * FROM job_resources_list
                WHERE id = {name_or_id}
            """
        elif type(name_or_id) is str:
            sql = f"""
                SELECT * FROM job_resources_list
                WHERE resources_name like '%{name_or_id}%'
            """
        if sql == '':
            return {}
        return self.query(sql)

    def get_jobs(self):
        sql = f"""
            SELECT * FROM jobs
        """
        return self.query(sql)

    def get_resources_by_job_id(self, job_id):
        sql = f"""
            SELECT * FROM job_resources_list
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

    def get_barrer(self, x, y):
        sql = f"""
            SELECT * FROM barrers
            WHERE x = {x} and
            y = {y};
        """
        return self.query(sql)

    def get_zaaps(self):
        sql = f"""
            SELECT * FROM zaaps
        """
        return self.query(sql)


if __name__ == '__main__':
    database = Database()
    sql = f"""SELECT * FROM monsters"""
    print(database.get_zaaps())
    # # sql = f"""SELECT * FROM monsters"""
    # # print(database.query(sql))
    # sql = f"""SELECT * FROM job_resources_locationa"""
    # print(database.query(sql))
    pass