from Model import Model
from utils import slog
import sqlite3

class TW(Model):
    def __init__(self, para):
        self.tw = para.get("tw", None)
        self.userid = para.get("userid", None)
        self.inittime = para.get("inittime", None)
        self.updatetime = para.get("updatetime", None)
        self.id = para.get("id", None)

        if self.tw is None or self.userid is None:
            raise Exception

        if self.inittime is None:
            self.inittime = self.now_time()

    def save(self):
        self.save_insert()

    def get_id(self):
        return self.id

    def save_insert(self):
        conn = self.get_conn()
        sql_insert = '''
                    INSERT INTO 
                    `TW`(tw, userid, inittime, updatetime)
                    VALUES (?,?,?,?)
                '''
        conn.execute(sql_insert, (self.tw, self.userid, self.inittime, self.updatetime))
        sql_select = '''
            SELECT MAX(id)
            FROM TW
        '''
        cursor = conn.execute(sql_select)
        for id in cursor:
            self.id = id
        conn.commit()





def create():
    conn = sqlite3.connect(TW.db_path())
    sql_create = '''
        CREATE TABLE `TW`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `tw` TEXT NOT NULL,
            `userid` INTEGER NOT NULL,
            `inittime` TEXT NOT NULL,
            `updatetime` TEXT
        )
    '''
    conn.execute(sql_create)

if __name__ == "__main__":
    d = dict(
        tw = "aaaa",
        userid = 2,
    )