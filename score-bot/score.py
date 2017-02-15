import re
from collections import Counter

import aiohttp
import asyncio
import async_timeout


async def get(session, url, loop):
    with async_timeout.timeout(10, loop=loop):
        async with session.get(url) as response:
            return await response.json()


async def get_names(loop, baseurl):
    files = list()
    async with aiohttp.ClientSession(loop=loop) as session:
        for x in await get(session, baseurl, loop):
            resp = await get(session, x['git_url'] + '?recursive=1', loop)
            files += [x['path'] for x in resp['tree']]
    names = Counter(re.findall(r"-(\w+).", x)[0] for x in files if '-' in x)
    return names.most_common()


def main():
    api_url = 'https://api.github.com'
    url = api_url + '/repos/devsoc/dailyprogrammer/contents/solutions'
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_names(loop, url))


if __name__ == '__main__':
    names = main()
    print(names)
