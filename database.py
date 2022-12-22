import sqlite3

class Database:

    def __init__(self,db:str) -> None:
        self.conn = sqlite3.connect(db,check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, time DATETIME, price FLOAT)")
        self.cur.execute('CREATE TABLE IF NOT EXISTS classifier (id INTEGER PRIMARY KEY, classification VARCHAR(4),rmse FLOAT,accuracy FLOAT,decision VARCHAR(10))')
        self.conn.commit()

    def view(self,table_name:str) -> list:
        if table_name == 'data':
            self.cur.execute("SELECT * FROM data ORDER BY id DESC LIMIT 60")
        elif table_name == 'classifier':
            self.cur.execute("SELECT * FROM classifier")
        
        row = self.cur.fetchall()
        return row
    
    def insert_tick(self,date:str, price:float) -> None:
        self.cur.execute("INSERT INTO data VALUES(NULL,?,?)",(date,price))
        self.conn.commit()
    
    def insert_classification(self, classifier:str, rmse:float, accuracy:float, decision:str) -> None:
        self.cur.execute("INSERT INTO classifier VALUES(NULL,?,?,?,?)",(classifier,rmse,accuracy,decision))
        self.conn.commit()

    def clear_table(self,table_name:str) -> None:
        self.cur.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()