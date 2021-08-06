# Autoloader
import sys
import os
from pathlib import Path
from threading import Lock

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            f"{root_path}{os.sep}database{os.sep}dofus_sqlite.db"
        )
        self.check_or_create_tables()
        self.insert_values()
        self.lock = Lock()


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
        cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"""
        )
        results = cursor.fetchall()
        cursor.close()
        for row in results:
            if row[0] == table_name:
                return True
        return False

    def check_or_create_tables(self):
        cursor = self.connection.cursor()
        tables = {
            "job_type": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        job_type TEXT UNIQUE
                    );
                """,
                "with_index": False,
            },
            "jobs": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        job_name TEXT UNIQUE,
                        job_type integer,
                        FOREIGN KEY(job_type) REFERENCES job_type(id)
                    );
                """,
                "with_index": False,
            },
            "harvestables_list": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        resources_name TEXT UNIQUE,
                        resources_level integer,
                        job_id integer,
                        FOREIGN KEY(job_id) REFERENCES jobs(id)
                    );
                """,
                "with_index": False,
            },
            "monsters": {
                "temp": False,
                "sql": """
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
                "with_index": False,
            },
            "drops": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        item_id integer PRIMARY KEY,
                        item_name TEXT,
                        item_level INTEGER,
                        monster_id INTEGER,
                        drop_rate REAL,
                        FOREIGN KEY(monster_id) REFERENCES monsters(id)
                    );
                """,
                "with_index": False,
            },
            "world_map": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id integer PRIMARY KEY,
                        x INTEGER,
                        y INTEGER,
                        outdoors INTEGER
                    );
                """,
                "with_index": False,
            },
            "interactives": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        world_map_id INTEGER,
                        type TEXT,
                        cell INTEGER,
                        offset_x INTEGER,
                        offset_y INTEGER,
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                "with_index": False,
            },
            "monsters_location": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        world_map_id INTEGER,
                        monster_id INTEGER REFERENCES monsters(monster_id),
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                "with_index": False,
            },
            "connections": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        origin INTEGER,
                        destiny INTEGER,
                        type INTEGER,
                        cell INTEGER,
                        offset_x INTEGER,
                        offset_y INTEGER,
                        FOREIGN KEY(origin) REFERENCES world_map(id),
                        FOREIGN KEY(destiny) REFERENCES world_map(id)
                    );
                """,
                "with_index": False,
            },
            "zaaps": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        world_map_id INTEGER,
                        cell INTEGER,
                        offset_x INTEGER,
                        offset_y INTEGER,
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id)
                    );
                """,
                "with_index": False,
            },
            "harvestables_cells": {
                "temp": False,
                "sql": """
                    CREATE TABLE *table*(
                        world_map_id INTEGER,
                        harvestable_id INTEGER,
                        cell INTEGER,
                        offset_x INTEGER,
                        offset_y INTEGER,
                        FOREIGN KEY(world_map_id) REFERENCES world_map(id),
                        FOREIGN KEY(harvestable_id) REFERENCES harvestables_list(id)
                    );
                """,
                "with_index": False,
            },
        }
        for table in tables:
            tables_to_create = [table]
            if tables[table]["temp"]:
                tables_to_create.append(f"{table}_temp")
            sql = tables[table]["sql"]
            for table_to_create in tables_to_create:
                if not self.check_if_tabel_exists(table_to_create):
                    create_table = sql.replace("*table*", table_to_create)
                    cursor.execute(create_table)
                    if tables[table]["with_index"]:
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
        cursor.execute(
            """INSERT OR IGNORE INTO jobs(job_name, job_type) VALUES (?, ?);""", row
        )
        self.connection.commit()

    def insert_harvestables_list(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO harvestables_list(resources_name, resources_level, job_id) VALUES (?, ?, ?);""",
            row,
        )
        self.connection.commit()

    def insert_monsters(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO monsters(monster_id, monster_name, monster_type, level, life_points, action_points, movement_points, pa_dodge, pm_dodge, earth_resistance, air_resistance, fire_resistance , water_resistance, neutral_resistance, can_trackle, can_be_pushed, can_switch_pos, can_switch_pos_on_target, can_be_carried) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
            row,
        )
        self.connection.commit()

    def insert_world_map(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO world_map(id, x, y, outdoors) values(?,?,?,?);""",
            row,
        )
        self.connection.commit()
        return cursor.lastrowid

    def insert_zaaps(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO zaaps(name, world_map_id, cell, offset_x, offset_y) values(?,?,?,?,?);""",
            row,
        )
        self.connection.commit()

    def insert_harvestables_cells(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO harvestables_cells(world_map_id, harvestable_id, cell, offset_x, offset_y) values(?,?,?,?,?);""",
            row,
        )
        self.connection.commit()

    def insert_drops(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO drops(item_id, item_name, item_level, monster_id, drop_rate) values(?,?,?,?,?);""",
            row,
        )
        self.connection.commit()

    def insert_interactives(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO interactives(world_map_id, type, cell, offset_x, offset_y) values(?,?,?,?,?);""",
            row,
        )
        self.connection.commit()

    def insert_monster_location(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO monsters_location(world_map_id, monster_id) values(?,?);""",
            row,
        )
        self.connection.commit()

    def insert_connector(self, row: tuple):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO connections(origin, destiny, type, cell, offset_x, offset_y) values(?,?,?,?,?,?);""",
            row,
        )
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
        cursor.execute(
            f"""UPDATE  world_map set {column_name} = ? where id = ?;""", row
        )
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

    def insert_values_executor(self, callback, values_list: list):
        for values in values_list:
            callback(values)

    def insert_values_job_type_2020_11_02(self):
        values_list = [
            ("drop_collecting",),
            ("collecting",),
        ]
        self.insert_values_executor(
            callback=self.insert_job_type, values_list=values_list
        )

    def insert_values_jobs_2020_11_02(self):
        values_list = [
            ("lumberjack", 2),
            ("farmer", 2),
            ("alchemist", 2),
            ("miner", 2),
            ("fishman", 2),
            ("Artificer", 1),
            ("Carver", 1),
            ("Handyman", 1),
            ("Jeweller", 1),
            ("Shoemaker ", 1),
            ("Smith", 1),
            ("Tailor", 1),
        ]
        self.insert_values_executor(callback=self.insert_jobs, values_list=values_list)

    def insert_value_harvestables_2021_05_02(self):
        values_list = [
            ("Ash", 1, 1),
            ("Chestnut", 20, 1),
            ("Walnut", 40, 1),
            ("Oak", 60, 1),
            ("Bombu", 70, 1),
            ("Maple", 80, 1),
            ("Oliviolet", 90, 1),
            ("Yew", 100, 1),
            ("Bamboo", 110, 1),
            ("Cherry", 120, 1),
            ("Hazel", 130, 1),
            ("Ebony", 140, 1),
            ("Kaliptus", 150, 1),
            ("Hornbeam", 160, 1),
            ("Dark Bamboo", 170, 1),
            ("Elm", 180, 1),
            ("Holy Bamboo", 190, 1),
            ("Aspen", 200, 1),
            ("Mahaquany", 200, 1),
            ("Wheat", 1, 2),
            ("Barley", 20, 2),
            ("Oats", 40, 2),
            ("Hop Hop", 60, 2),
            ("Flax", 80, 2),
            ("Rice", 100, 2),
            ("Rye Rye", 100, 2),
            ("Malt", 120, 2),
            ("Hemp", 140, 2),
            ("Corn", 160, 2),
            ("Millet", 180, 2),
            ("Frosteez", 200, 2),
            ("Quisnoa", 200, 2),
            ("Nettles", 1, 3),
            ("Sage", 20, 3),
            ("Five-Leaf Clover", 40, 3),
            ("Wild Mint", 60, 3),
            ("Freyesque Orchid", 80, 3),
            ("Edelweiss", 100, 3),
            ("Pandkin Seed", 120, 3),
            ("Ginseng", 140, 3),
            ("Belladonna", 160, 3),
            ("Mandrake", 180, 3),
            ("Salikronia", 200, 3),
            ("Snowdrop", 200, 3),
            ("Iron", 10, 4),
            ("Copper", 20, 4),
            ("Bronze", 40, 4),
            ("Cobalt", 60, 4),
            ("Manganese", 80, 4),
            ("Tin", 100, 4),
            ("Silicate", 100, 4),
            ("Silver", 120, 4),
            ("Bauxite", 140, 4),
            ("Gold", 160, 4),
            ("Dolomite", 180, 4),
            ("Obsidian", 200, 4),
            ("Sepiolite", 200, 4),
            ("Gudgeon", 1, 5),
            ("Grawn", 10, 5),
            ("Trout", 20, 5),
            ("Crab Surimi", 30, 5),
            ("Kittenfish", 40, 5),
            ("Breaded Fish", 50, 5),
            ("Ediem Carp", 60, 5),
            ("Shiny Sardine", 70, 5),
            ("Pike", 80, 5),
            ("Kralove", 90, 5),
            ("Eel", 100, 5),
            ("Grey Sea Bream", 110, 5),
            ("Perch", 120, 5),
            ("Blue Ray", 130, 5),
            ("Monkfish", 140, 5),
            ("Sickle-Hammerhead Shark", 150, 5),
            ("Lard Bass", 160, 5),
            ("Cod", 170, 5),
            ("Tench", 180, 5),
            ("Swordfish", 190, 5),
            ("Icefish", 200, 5),
            ("Limpet", 200, 5),
        ]
        self.insert_values_executor(
            callback=self.insert_harvestables_list, values_list=values_list
        )

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
            ("Way of Souls", 154010371, -1, -3),
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
        self.lock.acquire(blocking=True, timeout=-1)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.lock.release()
        return rows

    def get_world_map_with_harvestable_indication(self, harvestables_list: list):
        harvestables_list = [str(i) for i in harvestables_list]
        sql = f"""SELECT
                conn.origin,
                conn.destiny,
                CASE WHEN harv.quantity IS NULL THEN 0 ELSE harv.quantity END AS quantity,
                harv.harvestable_id
                FROM connections conn
                LEFT JOIN harvestables_location harv
                ON harv.world_map_id = conn.origin
                AND harv.harvestable_id IN ({','.join(harvestables_list)})"""
        return self.query(sql)

    def get_maps_with_harvestable_id(self, harvestable_id):
        sql = f"""SELECT harv.world_map_id
            FROM harvestables_location harv
            WHERE harv.harvestable_id = {harvestable_id}"""
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

    def get_connectors_by_origin_map_id(self, world_map_id: int):
        sql = f"""
            SELECT conn.id
            FROM connections conn
            WHERE conn.origin = {world_map_id}
        """
        result = [i[0] for i in self.query(sql)]
        return result

    def get_previous_connectors_by_connector_id(self, connection_id):
        sql = f"""
            SELECT conn.id from connections conn
            WHERE conn.destiny = (SELECT origin FROM connections WHERE id = {connection_id})
        """
        result = [i[0] for i in self.query(sql)]
        return result

    def get_next_connectors_by_connector_id(self, connection_id):
        sql = f"""
            SELECT conn.id from connections conn
            WHERE conn.origin = (SELECT destiny FROM connections WHERE id = {connection_id})
        """
        result = [i[0] for i in self.query(sql)]
        return result

    def get_connectors_by_destiny_map_id(self, destiny_map_id: int):
        sql = f"""
            SELECT conn.id
            FROM connections conn
            WHERE conn.destiny = {destiny_map_id}
        """
        result = [i[0] for i in self.query(sql)]
        return result

    def get_connector_info_by_id(self, connector_id: int):
        sql = f"""
            SELECT conn.origin, conn.destiny, conn.cell, conn.offset_x, conn.offset_y, conn.id
            FROM connections conn
            WHERE conn.id = {connector_id}
        """
        result = self.query(sql)
        return result[0]

    def get_map_info(self, world_map_id: int):
        sql = f"""
            SELECT world.id, world.x, world.y, world.outdoors
            FROM world_map world
            WHERE world.id = {world_map_id}
        """
        return self.query(sql)

    def get_zaaps(self):
        sql = """
            SELECT * FROM zaaps zaap
            WHERE zaap.name IS NOT NULL
        """
        return self.query(sql)

    def get_zaap_info_by_map_id(self, map_id: int):
        sql = f"""
            SELECT * FROM zaaps zaap
            WHERE zaap.world_map_id =  {map_id}
        """
        result = self.query(sql)
        return result[0]

    def get_harvestables_cells_by_map_id(self, harvestables: list, map_id: int):
        harvestables = [str(i) for i in harvestables]
        sql = f"""
            SELECT hc.cell, hc.offset_x, hc.offset_y FROM harvestables_cells hc
            WHERE hc.world_map_id = {map_id} AND
            hc.harvestable_id in ({', '.join(harvestables)})
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
                SELECT harv.world_map_id, harv.harvestable_id, count(*) as quantity
                FROM harvestables_cells harv
                GROUP BY harv.world_map_id, harv.harvestable_id
            """
        )
        self.connection.commit()


if __name__ == "__main__":
    database = Database()
    print(database.get_connector_info_by_id(9465))
