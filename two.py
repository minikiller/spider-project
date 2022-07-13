
import aiohttp,time
from asyncio import ensure_future, gather
import asyncio

async def request_controller(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [ensure_future(request_worker(session, url)) for url in urls]
        results = await gather(*tasks)
    return results

async def request_worker(session, url):
    async with session.get(url) as response:
        return await response.json()

start_time = time.time()
url = 'https://maps.kartoza.com/geoserver/wms?SERVICE=WMS&INFO_FORMAT=application%2Fjson&LAYERS=altitude&QUERY_LAYERS=altitude&FEATURE_COUNT=10&BBOX=31.396201370893717%2C-24.456190281345222%2C31.396398629106283%2C-24.45600971865369&WIDTH=101&HEIGHT=101&REQUEST=GetFeatureInfo&I=50&j=50'
urls = [url for i in range(100)]

for url in urls:
    print(url)

# loop = asyncio.get_event_loop()
# results = loop.run_until_complete(request_controller(urls))
# print(results[0])
print("--- %s seconds ---" % (time.time() - start_time))