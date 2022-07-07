import aiohttp
import asyncio
import time

start_time = time.time()

async def main():

    async with aiohttp.ClientSession() as session:

        # for number in range(1, 151):
        pokemon_url = f'https://randomuser.me/api'
        async with session.get(pokemon_url) as resp:
            data = await resp.json()
            print(data)

asyncio.run(main())
# asyncio.get_event_loop().run_until_complete(main())
print("--- %s seconds ---" % (time.time() - start_time))