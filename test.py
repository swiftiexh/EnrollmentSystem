from db.db_config import DB_CONFIG
import pymysql

try:
    conn = pymysql.connect(**DB_CONFIG)
    print("数据库连接成功！")
    conn.close()
except Exception as e:
    print("数据库连接失败：", e)
