import aiohttp
import asyncio
import time

start_time = time.time()
result=["hello","world","is me"]

async def main():

    async with aiohttp.ClientSession() as session:

        for number in range(1, 15):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                result.append(pokemon['name'])
    await pr()

async def pr():
    tasks=[]
    start_time = time.time()
    for value in result:
        task=asyncio.ensure_future(func(value))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print("--- %s seconds ---" % (time.time() - start_time))

async def func(str):
    print(":hello")
    await asyncio.sleep(1)
    print(str)

asyncio.run(main())
# asyncio.get_event_loop().run_until_complete(main())
# print("--- %s seconds ---" % (time.time() - start_time))