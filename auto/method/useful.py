import configparser
import os


def ini(filepath: str) -> 'config':
    """读取ini配置文件，传入参数为文件路径（字符串格式），返回config对象，可对该对象使用config.get(section,name)方法取得相应的参数"""
    config = configparser.ConfigParser()
    config.read(filepath, encoding='utf-8')
    return config