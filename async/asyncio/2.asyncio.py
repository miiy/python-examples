import asyncio


async def sumx(id, num):
    await asyncio.sleep(1)
    return id+num


async def main():
    L = await asyncio.gather(
        sumx(1, 1),
        sumx(2, 2),
        sumx(3, 3),
    )
    print(L)

asyncio.run(main))
