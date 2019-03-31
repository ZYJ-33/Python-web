import sqlite3
import hashlib
import time
from utils import slog

def get_kl_vl(**kwargs):
    keys = kwargs.keys()
    values = kwargs.values()
    kl = []
    vl = []
    for key in keys:
        kl.append(key)
    for value in values:
        vl.append(value)
    return kl,vl


class Model(object):
    @classmethod
    def db_path(cls):
         path = ""                                 //需要指定一个path座位sqlite数据库的路径
         if path == "":
            raise Exception                       

    @classmethod
    def table_name(cls):
        return cls.__name__

    @classmethod
    def objetify(cls, ds):
        os = [cls(d) for d in ds]
        return os

    @classmethod
    def sha256_salted(cls, str, salt):
        def sha256_hash(str):
                return hashlib.sha256(str.encode("ascii")).hexdigest()
        str = sha256_hash(str)
        str = sha256_hash(str+salt)
        slog(str)
        return str

    @classmethod
    def now_time(cls):
        time_for = "%y/%m/%d %H:%M:%S"
        t = time.strftime(time_for, time.localtime(time.time()))
        return t

    @classmethod
    def get_conn(cls):
        conn = sqlite3.connect(cls.db_path())
        return conn

    @classmethod
    def find_by(cls, **kwargs):                                         //涉及到kwargs的都只支持一个 key-value 形式的数据库查找
        ds = []
        conn = cls.get_conn()
        for k, v in kwargs.items():
            key = k
            value = v
        sql_select = '''
                               SELECT *
                               FROM {} t
                               WHERE t.{} = ?
                           '''.format(cls.table_name(),key)
        cursor = conn.execute(sql_select, (value,))
        cursor.row_factory = dict_factory
        for row in cursor:
            ds.append(row)
        conn.commit()
        return ds

    @classmethod
    def find_all(cls):
        ds = []
        conn = cls.get_conn()
        sql_select = '''
                               SELECT *
                               FROM {} 
                           '''.format(cls.table_name())
        cursor = conn.execute(sql_select)
        cursor.row_factory = dict_factory
        for row in cursor:
            ds.append(row)
        conn.commit()
        return ds

    @classmethod
    def todelete(cls, **kwargs):
        conn = cls.get_conn()
        for k, v in kwargs.items():
            key = k
            value = v
        sql_delete = '''
                               DELETE
                               FROM {}
                               WHERE {} = ?
                           '''.format(cls.table_name(), key)
        conn.execute(sql_delete, (value,))
        conn.commit()

    @classmethod
    def toupdate(cls, **kwargs):
        conn = cls.get_conn()
        kl, vl = get_kl_vl(**kwargs)
        slog(kl,vl)
        sql_update = '''
                        UPDATE {}
                        SET {} = ?
                        WHERE {} = ?
                                   '''.format(cls.table_name(), kl[0], kl[1])
        conn.execute(sql_update, tuple(vl))
        conn.commit()

    @classmethod
    def todelete(cls, **kwargs):
        conn = cls.get_conn()
        for k, v in kwargs.items():
            key = k
            value = v
        sql_delete = '''
                                DELETE
                                FROM {}
                                WHERE {} = ?
                            '''.format(cls.table_name(), key)
        conn.execute(sql_delete, (value,))
        conn.commit()



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



if __name__ == "__main__":
    pass
