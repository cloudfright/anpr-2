import sqlite3
import logging

class EventPersistence:

    EVENTS_DB = "./data/events.db"
    EVENTS_TABLE = "events"
 
    def __init__(self):
        self.db_name = EventPersistence.EVENTS_DB
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS events(                                    
                timestamp INT PRIMARY KEY,      
                img_filename TEXT,
                ocr_result TEXT);
            """)
            self.conn.commit()
        except Exception as e:
            logging.critical(f"Error creating events table - {e}")

    def record_event(self, timestamp, img_filename, ocr_result):
        try:
            ts = round(timestamp * 1000)
            self.cursor.execute(f"INSERT INTO {EventPersistence.EVENTS_TABLE} VALUES ({ts}, {img_filename}, {ocr_result});")
            self.conn.commit()
        except Exception as e:
            logging.critical(f"Error inserting event - {e}")

    def  get_events(self, start_ts, end_ts):
        try:
            start_ts = round(start_ts * 1000)
            end_ts = round(end_ts * 1000)
            self.cursor.execute(f"SELECT timestamp, img_filename, ocr_result FROM {EventPersistence.EVENTS_TABLE} WHERE timestamp >= {start_ts} AND timestamp <= {end_ts};")
            return self.cursor.fetchall()
        except Exception as e:
            logging.critical(f"Error getting events - {e}")
            return None
    
    def  query_events(self, select_query, where_query):
        try:
            if len(select_query) == 0:
                raise  ValueError("select_query cannot be empty")
            
            if len(where_query) == 0:
                raise  ValueError("where_query cannot be empty")
            
            self.cursor.execute(f"SELECT {select_query} FROM {EventPersistence.EVENTS_TABLE} WHERE {where_query};")
            return self.cursor.fetchall()
        except Exception as e:
            logging.critical(f"Error querying events - {e}")
            return None

    def  delete_events(self, start_ts, end_ts):
        try:
            self.cursor.execute(f"DELETE FROM {EventPersistence.EVENTS_TABLE} WHERE timestamp >= {start_ts} AND timestamp <= {end_ts};")
            self.conn.commit()
        except Exception as e:
            logging.critical(f"Error deleting events - {e}")

    def close(self):
        self.conn.close()