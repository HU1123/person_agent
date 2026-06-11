"""进程内令牌桶限流。"""

import time


class TokenBucket:
    """简单令牌桶：capacity 为桶容量，refill_rate 为每秒补充令牌数。"""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def try_acquire(self, tokens: float = 1.0) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def acquire_or_raise(self, tokens: float = 1.0) -> None:
        if not self.try_acquire(tokens):
            raise RateLimitExceeded("请求过于频繁，请稍后再试")


class RateLimitExceeded(Exception):
    """限流拦截。"""
