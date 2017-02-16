import re
import json
import base64
from collections import Counter

import aiohttp
import asyncio
import async_timeout

import settings


async def get(session, url, loop):
    with async_timeout.timeout(10, loop=loop):
        async with session.get(url) as response:
            return await response.json()


async def get_names(session, loop, baseurl):
    files = list()
    for x in await get(session, baseurl, loop):
        resp = await get(session, x['git_url'] + '?recursive=1', loop)
        files += [x['path'] for x in resp['tree']]
    names = Counter(re.findall(r"-(\w+).", x)[0] for x in files if '-' in x)
    return names.most_common()


async def update_readme(session, scores, loop, api_url):
    url = api_url + '/repos/devsoc/dailyprogrammer/contents/README.md'
    resp = await get(session, url, loop)
    sha = resp['sha']

    new_readme = list()
    print(scores)
    readme = base64.b64decode(resp['content']).decode()
    for line in readme.split('\n'):
        new_readme.append(line)
        if '| ------------- |' in line:
            new_readme += ['| ' + n + ' | ' + str(s) + ' |' for n, s in scores]
    new_readme = '\n'.join(new_readme)
    print(new_readme)

    commit = {
        'committer': {'name': 'Bot', 'email': 'programmer.arsh@gmail.com'},
        'sha': sha,
        'message': '[Bot commit] testing api',
        'content': base64.b64encode(new_readme.encode()).decode()
    }
    print(commit)

    print(url)
    url += '?access_token=' + settings.token
    async with session.put(url, data=json.dumps(commit)) as resp:
        r = await resp.json()
    print(r)


async def main(loop):
    api_url = 'https://api.github.com'
    url = api_url + '/repos/devsoc/dailyprogrammer/contents/solutions'
    async with aiohttp.ClientSession(loop=loop) as session:
        scores = await get_names(session, loop, url)
        return await update_readme(session, scores, loop, api_url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
