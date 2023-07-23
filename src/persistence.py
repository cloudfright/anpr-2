import sqlite3
import logging

class EventPersistence:

    EVENTS_DB = "./data/events.db"
    EVENTS_TABLE = "events"
 
    def __init__(self):
        self.db_name = EventPersistence.EVENTS_DB
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events(                                    
            timestamp INT PRIMARY KEY,      
            img_filename TEXT,
            ocr_result TEXT);
        """)
        self.conn.commit()

    def record_event(self, timestamp, img_filename, ocr_result):
        try:
            ts = round(timestamp * 1000)
            self.cursor.execute("INSERT INTO events VALUES (?, ?, ?);", (ts, img_filename, ocr_result))
            self.conn.commit()
        except Exception as e:
            logging.critical(f"Error inserting event - {e}")

    def  get_events(self, start_ts, end_ts):
        try:
            start_ts = round(start_ts * 1000)
            end_ts = round(end_ts * 1000)
            self.cursor.execute("SELECT timestamp, img_filename, ocr_result FROM events WHERE timestamp >= ? AND timestamp <= ?;", (start_ts, end_ts))
            return self.cursor.fetchall()
        except Exception as e:
            logging.critical(f"Error getting events - {e}")
            return None
        
    def close(self):
        self.conn.close()
"""

          # self.cursor.execute("SELECT timestamp FROM events WHERE timestamp >= ? AND timestamp <= ?;", (start_ts, end_ts))
 
    def insert(self, table_name, values):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({values})")
        self.conn.commit()

    def select(self, table_name, columns, condition):
        self.cursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        return self.cursor.fetchall()

    def update(self, table_name, columns, condition):
        self.cursor.execute(f"UPDATE {table_name} SET {columns} WHERE {condition}")
        self.conn.commit()

    def delete(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()


"""