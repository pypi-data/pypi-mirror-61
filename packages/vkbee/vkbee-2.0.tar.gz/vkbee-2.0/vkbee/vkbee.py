# -*- coding: utf-8 -*-
# author: asyncvk

import six
import aiohttp
import requests
import time
import asyncio

"""
:authors: sergeyfilippov1, YamkaFox
:license: Mozilla Public License, version 2.0, see LICENSE file
:copyright: (c) 2020 asyncvk
"""

class VkApi:
    def __init__(self, token, loop, api_version="5.103"):
        self.token = token
        self.api_version = api_version

        self.base_url = "https://api.vk.com/method/"
        self.s = aiohttp.ClientSession()

        self.last_request_time = 0
        self.start_time = time.time()
        self.request_count = 0

    async def call(self, method_name, data):
        data["access_token"] = self.token
        data["v"] = self.api_version

        url = self.base_url + method_name
        self.request_count += 1

        self.last_request_time = time.time()
        r = await self.s.post(url, data=data)

        r = await r.json()

        if "error" in r:
            raise api_error(
                f'{r["error"]["error_msg"]} ({r["error"]["error_code"]})')

        return r["response"]

    def sync_call(self, method_name, data):
        data["access_token"] = self.token
        data["v"] = self.api_version

        url = self.base_url + method_name
        r = requests.post(url, data=data).json()

        if "error" in r:
            raise api_error(
                f'{r["error"]["error_msg"]} ({r["error"]["error_code"]})')

        return r

    def get_api(self):
        return ApiMethod(self)


class ApiMethod:

    __slots__ = ('_vk', '_method')

    def __init__(self, vk, method=None):
        self._vk = vk
        self._method = method

    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return ApiMethod(
            self._vk,
            (self._method + '.' if self._method else '') + method
        )

    async def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return await self._vk.call(self._method, kwargs)
