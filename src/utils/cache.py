import functools

class _MemCache:
    enabled = True
    _store  = {}
    def get(self, k):        return self._store.get(k)
    def set(self, k, v, ttl=None): self._store[k] = v
    def clear(self):         self._store.clear()

cache = _MemCache()

def cached(ttl=300, key_prefix=""):
    def dec(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            return fn(*a, **kw)
        return wrapper
    return dec
