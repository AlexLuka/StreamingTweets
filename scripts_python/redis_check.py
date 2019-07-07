import time
import redis
import pickle
from datetime import datetime


rc = redis.Redis(host='localhost', port=6379, db=0)

# Write a single value
# rc.set('foo', 'bar')
print('TEST: ', rc.get('foo'))

#
# Write a list
# timestamp1 = int(time.mktime(datetime.now().timetuple()))
# rc.lpush('simple list', pickle.dumps((timestamp1, '1')))
#
# time.sleep(2)
# timestamp2 = int(time.mktime(datetime.now().timetuple()))
# rc.lpush('simple list', pickle.dumps((timestamp2, '2')))
# rc.lpush('simple list', '3')

# val = rc.lrange("simple list", 0, 1)
#
# for v in val:
#     ts, var = pickle.loads(v)
#     print(f'timestamp: {ts}, variable: {var}, type={type(var).__name__}')

# rc.incr('MMM', 1)

print("Tweeters from Texas: ", rc.get('USA:TX:CITY:the'))
print("Tweeters from California: ", rc.get('USA:CA:CITY:the'))
