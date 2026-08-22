
class DistributedRateLimiter:
    """
    Adapter boundary for Redis-backed rate limiting. Falls back to local limiter.
    """
    def __init__(self,local_limiter,redis_client=None):
        self.local=local_limiter;self.redis=redis_client
    def allow(self,key,limit):
        if self.redis is None:return self.local.allow(key,limit)
        bucket=f"topospace:rl:{key}"
        n=self.redis.incr(bucket)
        if n==1:self.redis.expire(bucket,60)
        return n<=limit
