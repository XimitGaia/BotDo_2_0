import asyncio
import time
import threading

d = []
async def a():
    i = 0
    while i < 100:
        await asyncio.sleep(0)
        print(f"a: {i}")
        i += 2
    d.append("a")


async def b():
    i = 0
    while i < 100:
        await asyncio.sleep(0)
        print(f"b: {i}")
        i += 1
    d.append("b")

async def f():
    while len(d) == 0:
        await asyncio.sleep(0)
    return d[0]


def k():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(a())
    asyncio.ensure_future(b())
    loop.run_until_complete(f())

thread = threading.Thread(target=k, args=())
thread.start()

time.sleep(10)
