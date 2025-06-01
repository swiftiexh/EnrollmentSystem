# 统一数据库操作封装 
import pymysql
from db.db_config import DB_CONFIG

class DBManager:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
    
    #查：获取第一条记录
    def fetchone(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    #查：获取全部记录
    def fetchall(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    #执行增、删、改
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)
        self.conn.commit()

    # 开启事务
    def begin(self):
        self.conn.begin()

    # 提交事务
    def commit(self):
        self.conn.commit()

    # 回滚事务
    def rollback(self):
        self.conn.rollback()

    #关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()
    