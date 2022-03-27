from time import time

import requests
import asyncio
import aiohttp


def get_file(url):
    resp = requests.get(url, allow_redirects=True)
    return resp


def write_file(resp):
    filename = resp.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(resp.content)


def sync_main():
    t0 = time()
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

    print(time() - t0)


# if __name__ == '__main__':
#     sync_main()

#########################################

def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time()*1000))
    with open (filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as resp:
        data = await resp.read()
        write_image(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = list()

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    t0 = time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main2())
    print(time() - t0)
