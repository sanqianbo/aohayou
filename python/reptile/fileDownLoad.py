# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import os
import base64
from cryptography.fernet import Fernet
import aiohttp
import asyncio

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
keystr = "X0JxSkg4NFVBQVBPODlUM0VzT1liNnloeWtLcndkSldRT2xURzQ4MEM5RT0="


def get_aes_key():
    key = base64.b64decode(keystr).decode("utf8")
    return key


cipher = Fernet(get_aes_key())


def aes_cbc_decrypt(message):
    '''解密'''
    decrypted_text = Fernet(base64.b64decode(keystr).decode("utf8")).decrypt(
        bytes("{}".format(message), encoding="utf8"))
    return decrypted_text.decode("utf8")


def aes_cbc_encrypt(message):
    '''解密'''
    encrypted_text = cipher.encrypt(bytes("{}".format(message), encoding="utf8"))
    return encrypted_text


async def fetch(session, url, dst, pbar=None, headers=None):
    if headers:
        async with session.get(url, headers=headers) as req:
            with(open(dst, 'ab')) as f:
                while True:
                    chunk = await req.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    pbar.update(1024)
            pbar.close()
    else:
        async with session.get(url) as req:
            return req


async def async_download_from_url(url, dst):
    '''异步'''
    async with aiohttp.connector.TCPConnector(limit=300, force_close=True, enable_cleanup_closed=True) as tc:
        async with aiohttp.ClientSession(connector=tc) as session:
            req = await fetch(session, url, dst)

            file_size = int(req.headers['content-length'])
            print(f"获取视频总长度:{file_size}")
            if os.path.exists(dst):
                first_byte = os.path.getsize(dst)
            else:
                first_byte = 0
            if first_byte >= file_size:
                return file_size
            header = {"Range": f"bytes={first_byte}-{file_size}"}
            pbar = tqdm(
                total=file_size, initial=first_byte,
                unit='B', unit_scale=True, desc=dst)
            await fetch(session, url, dst, pbar=pbar, headers=header)

    #

    # req = requests.get(url, headers=header, stream=True)


def download_from_url(url, dst):
    '''同步'''
    response = requests.get(url, stream=True)
    file_size = int(response.headers['content-length'])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": f"bytes={first_byte}-{file_size}"}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == '__main__':
    url = "http://ggkkmuup9wuugp6ep8d.exp.bcevod.com/mda-km671xd58s1yy16y/mda-km671xd58s1yy16y.mp4" #一个mp4链接即可。
    # task = [asyncio.ensure_future(async_download_from_url(url, f"{i}.mp4")) for i in range(2, 14)]
    #     # try:
    #     #     loop = asyncio.get_event_loop()
    #     #     loop.run_until_complete(asyncio.wait(task))
    #     # except:
    #     #     loop.run_until_complete(loop.shutdown_asyncgens())
    #     # finally:
    #     #     loop.close()
    # download_from_url(url, "1.mp4")
