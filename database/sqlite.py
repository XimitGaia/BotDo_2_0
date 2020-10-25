import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('.\dofus_sqlite.db')
        self.check_or_create_tables()
    
    def check_or_create_tables(self):
        cursor = self.connection.cursor()
        tables = {
            'training_results': {
                'temp': True,            
                'sql':  """
                    CREATE TABLE IF NOT EXISTS *table*
                    (
                        id TEXT NOT NULL,
                        match_count REAL,
                        color_count REAL,
                        group_count REAL,
                        saturation_count REAL,
                        bright_count REAL,
                        total_matches INTEGER,
                        total_miss_matches INTEGER,
                        time REAL
                    );
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
    
    def insert_training_results(self, row: tuple)-> str:
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO training_results_temp(id, match_count, color_count, group_count, saturation_count, bright_count, total_matches, total_miss_matches, time) VALUES (?,?,?,?,?,?,?,?,?)""",row)
        self.connection.commit()

if __name__ == '__main__':
    database = Database()