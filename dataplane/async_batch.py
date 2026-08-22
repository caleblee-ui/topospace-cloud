
from __future__ import annotations
import asyncio

class AsyncBatchOptimizer:
    def __init__(self, engine, max_concurrency=32):
        self.engine=engine
        self.sem=asyncio.Semaphore(max_concurrency)

    async def optimize_one(self, request):
        async with self.sem:
            loop=asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: self.engine.optimize_adaptive(**request))

    async def optimize_batch(self, requests):
        return await asyncio.gather(*(self.optimize_one(r) for r in requests))
