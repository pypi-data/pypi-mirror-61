import os
from datetime import datetime
import sqlite3

class logger:
    def __init__(self, path="logs", mode="debug", sensibility=0):
        self.sensibility=sensibility
        self.path=path
        self.mode=mode
        try:
            self.currentLog=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            try:
                os.mkdir(self.path)
            except:
                pass
            self.log=open(f"{self.path}/log {self.currentLog}.txt", "a")
            self.log.write("logs start\n")
            self.log.close()
            
        except:
            pass
        try:
            conn = sqlite3.connect(f"{path}/log {self.currentLog}.dblog")
            c = conn.cursor()
            c.execute('CREATE TABLE log (level INTEGER, info text)')
            conn.commit()
            conn.close()
        except:
            pass
        

    def write(self, level:int, text:str):
        try:
            if self.mode=="debug":
                print(f"log: {level} |{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}| {text}\n")
            if level>=self.sensibility:
                level=str(level)
                self.log.write(f"{level} |{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}| {text}\n")
                self.log.close
                conn = sqlite3.connect(f"{self.path}/log {self.currentLog}.dblog")
                c = conn.cursor()
                c.execute(f"INSERT INTO log VALUES ('{level}','{text}')")
                conn.commit()
                conn.close()

            return 0
        except Exception as e :
            print(e)
            return Exception
    
