import json
import time

def writeFile(jsonFormattedAray, fileName):
    with open(fileName, 'a+') as outfile:
        json.dump(jsonFormattedAray, outfile)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap