'''
Author: bananalone
Date: 2024-01-03
Copyright (c) 2024 by bananalone, All Rights Reserved.
'''


import json
from typing import (
    Any, 
    Iterator,
    AsyncIterable
)

import requests
import aiohttp
from fastapi.responses import StreamingResponse


def post(url: str, payload: Any, headers: dict = None):
    headers = _create_headers(headers)
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def stream_post(url: str, payload: Any, headers: dict = None):
    headers = _create_headers(headers)
    response = requests.post(url, json=payload, headers=headers, stream=True)
    for chunk in response.iter_content(chunk_size=1024):
        chunk_obj = json.loads(chunk)
        yield chunk_obj


async def apost(
    session: aiohttp.ClientSession,
    url: str,
    payload: Any,
    headers: dict = None,
):
    headers = _create_headers(headers)
    async with session.post(url, json=payload, headers=headers) as resp:
        return resp.json()


async def astream_post(
    session: aiohttp.ClientSession,
    url: str,
    payload: Any,
    headers: dict = None,
):
    async with session.post(url, json=payload, headers=headers) as resp:
        async for chunk, _ in resp.content.iter_chunks():
            # 最后一个 chunk 为 b'', end 为 True, 只能采用 len(chunk) > 0 的方式判断是否结束
            if len(chunk) > 0:
                # server send event (data only) 方式获取服务器传输的数据. data: {data}\n\n
                data = chunk[5:].strip()
                yield json.loads(data)


def _create_headers(headers: dict | None):
    if headers:
        return {
            'Content-Type': 'application/json',
            **headers,
        }
    return {'Content-Type': 'application/json'}


def EventSourceResponse(content: AsyncIterable[str | bytes] | Iterator[str | bytes]) -> StreamingResponse:
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    if isinstance(content, Iterator):
        def _content(content: Iterator[str | bytes]):
            for chunk in content:
                yield _chunk_to_data(chunk)

        return StreamingResponse(_content(content), headers=headers)
    else:
        async def _async_content(content: AsyncIterable[str | bytes]):
            async for chunk in content:
                yield _chunk_to_data(chunk)

        return StreamingResponse(_async_content(content), headers=headers)


def _chunk_to_data(chunk: str | bytes) -> bytes:
    if isinstance(chunk, bytes):
        data = b'data: ' + chunk + b'\n\n'
    else:
        data = f'data: {chunk}\n\n'.encode(encoding='utf-8')
    return data


