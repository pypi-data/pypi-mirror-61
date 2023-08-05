# coding: utf-8
import os

"""
配置集合
author:CallMeE
date:2018-06-01
"""

project_root = os.getcwd()

# 服务器相关配置
server_threaded = False  # 服务器多线程开关
server_processes = 1  # 服务器多进程处理

debug_trace = False  # 调试跟踪记录

# 此为开启ip防火墙模式(1秒不超过50次请求,60秒解冻)
ip_count = False

# rps监控配置(默认关闭)
rps = False
# rps默认100ps
rps_max = 100

# 此处为服务器配置
host = '127.0.0.1'
port = 88
ssl_context = 'adhoc'

# 此处为路由文件夹配置
blueprint_path = ['/routes']  # route model dir path

# 默认使用DOPHON封装的python.logging,可选HUES
log_types = 'DOPHON'

# 此处为日志配置
if debug_trace:
    logger_config = {
        # 'filename': 'app.log',
        # 'level': 'logging.DEBUG',
        'format': '%(levelname)s : <%(module)s> (%(asctime)s) ==> %(filename)s {%(funcName)s} [line:%(lineno)d] ::: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }

# 错误信息类型配置
error_info = 'HTML'

# 组件路径
components_path = ['/']

# 默认关闭接口文档展示
load_desc = False
