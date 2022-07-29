import configparser
import os
import sys


def getModuleName():
    # 获取当前文件名
    key = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
    value = config['DEFAULT'][key]
    # 创建文件夹
    if not os.path.exists(value):
        os.mkdir(value)
    return value
