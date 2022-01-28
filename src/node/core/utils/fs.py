import os
import ujson

__FILE_PATH = 'node/config.json'

def read():
    f = open(__FILE_PATH,'r')
    data_str=f.read()
    f.close()
    return ujson.loads(data_str)
    
def write(data):
    f = open(__FILE_PATH,'w+')
    f.write(ujson.dumps(data))
    f.close()
    

def remove():
    os.remove(__FILE_PATH)