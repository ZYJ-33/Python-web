from Model import Model
import sqlite3
from utils import slog
from Model import dict_factory

class User(Model):
    salted = "y2jd9"
    def __init__(self, para):
        self.username = para.get("username", None)
        self.password = para.get("password", None)
        self.id = para.get("id", None)


    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def register(self):            ##把从Request中得到的用户名和经哈希后的密码insert到数据库
        salted_pass = self.sha256_salted(self.password, self.salted)
        username = self.username
        try:
            self.insert(username, salted_pass)
            return True
        except sqlite3.IntegrityError:
            return False


    def insert(self, username, password):
        conn = self.get_conn()
        sql_insert = '''
            INSERT INTO 
            `User`(username,password)
            VALUES (?,?)
        '''
        conn.execute(sql_insert, (username, password))
        conn.commit()

    @classmethod
    def login(cls, para):
        list = []
        username = para["username"]
        password = para["password"]
        password = cls.sha256_salted(password, cls.salted)
        cursor = cls.login_select(username, password)
        cursor.row_factory = dict_factory
        for row in cursor:
            list.append(row)

        return list
        '''
        if len(rows)>0:
            return True
        else:
            return False
        '''

    @classmethod
    def login_select(cls, username, password):
        conn = cls.get_conn()
        sql_select = '''
            SELECT *
            FROM User u
            WHERE u.username = ? AND u.password = ?
        '''
        cursor = conn.execute(sql_select, (username,password))
        conn.commit()
        return cursor



def create(conn):
    sql_create = '''
        CREATE TABLE `User`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `username` TEXT NOT NULL,
            `password` TEXT NOT NULL
        )
    '''
    conn.execute(sql_create)

if __name__ == "__main__":
   dict = {
       "username":"aaaa",
       "password":"abc"
   }
   u = User(dict)