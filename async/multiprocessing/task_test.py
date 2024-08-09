import asyncio

class Queue:
    def __init__(self):
        self.queue = []
        self.current = 0
        self.lock = asyncio.Lock()

    def enqueue(self, item):
        async with self.lock:
            self.queue.append(item)
            self.current += 1

    def dequeue(self):
        async with self.lock:
            if len(self.queue) > 0:
                return self.queue.pop()
            else:
                print("Queue is empty")


async def sum_num(a, b):
    await asyncio.sleep(1)
    return a + b


async def producer(queue):
    for i in range(1, 4):
        await asyncio.sleep(1)
        queue.enqueue(i)

async def main():
    img_queue = ImgQueue()

    tasks = []
    for i in range(1, 4):
        task = sum_num(i, i)
        tasks.append(task)
    L = await asyncio.gather(*tasks)
    print(L)

asyncio.run(main())
