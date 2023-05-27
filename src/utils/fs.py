import os
import ujson

__FILE_PATH = 'config.json'

def read():
    f = open(__FILE_PATH,'r')
    data_str=f.read()
    f.close()
    return ujson.loads(data_str)