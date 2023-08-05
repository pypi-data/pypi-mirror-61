# encoding:utf-8
import os

# 此处为数据库配置
project_root = os.getcwd()
pool_conn_num = 5  # size of db connect pool
pydc_host = 'localhost'
pydc_port = 3306
pydc_user = 'root'
pydc_password = 'root'
pydc_database = 'db'
pydc_xmlupdate_sech = False
db_mode = 'ALL'  # 数据库模式默认单例与分片兼容
db_pool_exe_time = False
orm_pre_load = False  # 对象映射管理器初始化是否连带初始化数据表

# 此处为分片数据库配置
db_cluster = [
    # {
    #     'alias': 'a',
    #     'host': 'localhost',
    #     'port': 3306,
    #     'database': 'db',
    #     'user': 'root',
    #     'password': 'root'
    # }
]

pool_ping = 7
