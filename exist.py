import asyncio

async def main(str):
    print("hello")
    await asyncio.sleep(1)
    print("world "+str)



async def hello():
    tasks=[]
    tasks.append(asyncio.ensure_future(main("first")))
    tasks.append(asyncio.ensure_future(main("second")))
    await asyncio.gather(*tasks)

asyncio.run(hello())

x=(i for i in range(100))
print(next(x))
