from Model import Model
from utils import slog
import sqlite3
from Model import dict_factory

class Comment(Model):
    def __init__(self, para):
        self.comment = para.get("comment", None)
        self.userid = para.get("userid", None)
        self.twid = para.get("twid", None)

        self.inittime = para.get("inittime", None)
        self.id = para.get("id", None)

        if self.comment is None or self.userid is None or self.twid is None:
            raise Exception

        if self.inittime is None:
            self.inittime = self.now_time()

    def get_id(self):
        return self.id

    def save(self):
        conn = self.get_conn()
        sql_insert = '''
                       INSERT INTO 
                       `Comment`(userid, twid, comment, inittime)
                       VALUES (?,?,?,?)
                   '''
        conn.execute(sql_insert, (self.userid, self.twid, self.comment, self.inittime))
        sql_select = '''
               SELECT MAX(id)
               FROM TW
           '''
        cursor = conn.execute(sql_select)
        for id in cursor:
            self.id = id
        self.id = self.id[0]
        conn.commit()

    @classmethod
    def find_by_twid(cls, twid):
        l = []
        conn = cls.get_conn()
        sql_select = '''
        SELECT  u.username,c.id,c.comment
        FROM Comment c, User u
        WHERE c.twid=? AND c.userid = u.id
        '''
        cursor = conn.execute(sql_select, (twid,))
        cursor.row_factory = dict_factory
        for row in cursor:
            l.append(row)
        return l


def create():
    conn = sqlite3.connect(Comment.db_path())
    sql_create = '''
        CREATE TABLE `Comment`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `userid` INTEGER NOT NULL,
            `twid` INTEGER NOT NULL,
            `comment` TEXT NOT NULL,
            `inittime` TEXT NOT NULL
        )
    '''
    conn.execute(sql_create)

if __name__ == "__main__":
    pass