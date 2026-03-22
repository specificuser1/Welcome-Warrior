import time

class Cache:

    def __init__(self):
        self.data = {}

    def set(self, key, value, ttl=60):
        expire = time.time() + ttl
        self.data[key] = (value, expire)

    def get(self, key):
        value = self.data.get(key)

        if not value:
            return None

        val, exp = value

        if time.time() > exp:
            del self.data[key]
            return None

        return val


cache = Cache()