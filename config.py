import configparser
import os,sys


def getModuleName():
    # 获取当前文件名
    key=os.path.splitext(os.path.basename(sys.argv[0]))[0]
    config = configparser.ConfigParser()
    config.read("config.ini")
    value = config['DEFAULT'][key]
    # 创建文件夹
    if not os.path.exists(value):
        os.mkdir(value)
    return value