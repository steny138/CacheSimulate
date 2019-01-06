
from ext import redis_store, mongo, cache
from log import HitLog

class Source(object):

    def __init__(self, county, distric, purpose, price_low, price_high):
        self.county = county
        self.distric = distric
        self.purpose = purpose
        self.price_low = price_low
        self.price_high = price_high
        self.source_type = "none"
        self.cache_key = f"{county}::{distric}{purpose}{price_low}{price_high}"
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.cache_key)

    def get_value(self):
        """取得來源資料
        """

        val = self.__get_cache_data(self.county, self.distric, self.purpose, self.price_low, self.price_high)
        
        log = HitLog(value= val + self.source_type, **self.__dict__)

        self.__add_log(log)

        return val

    def __get_cache_data(self, county, distric, purpose, price_low, price_high):
        val = self.cache_key

        if self.cache_key in cache:
            # 有熱點快取
            self.source_type = "memory"
            val = cache[self.cache_key]

        elif redis_store.get(self.cache_key):
            # 有分散式快取
            self.source_type = "redis"        
            val = bytes.decode(redis_store.get(self.cache_key))
            
        else:
            # 從資料庫取資料
            self.source_type = "database"
            # 取資料後 寫入redis內
            redis_store.set(self.cache_key, self.cache_key)
            redis_store.expire(self.cache_key, 60)
        
        return val

    def __add_log(self, log):
        """加入取得資料的Log紀錄
        """
        mongo.db.logs.insert_many([log.__dict__])


        