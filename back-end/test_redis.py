from redis import Redis
from pottery import RedisDict

redis = Redis.from_url('redis://localhost:6379')

tel = RedisDict({'jack': 4098, 'sape': 4139}, redis=redis, key='tel')