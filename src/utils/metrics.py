import functools

class _Counter:
    def labels(self, **kw): return self
    def inc(self, n=1):     pass

optimization_runs_total = _Counter()
quantum_advantage_total = _Counter()

def track_api_request(path, method):
    def dec(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw): return fn(*a, **kw)
        return wrapper
    return dec

def record_quantum_advantage(city): pass
def get_metrics(): return "# no metrics"
