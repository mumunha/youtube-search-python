import httpx
import os

from youtubesearchpython.core.constants import userAgent

class RequestCore:
    def __init__(self):
        self.url = None
        self.data = None
        self.timeout = 2
        # Convert proxy settings to transport format
        transport = httpx.HTTPTransport()
        http_proxy = os.environ.get("HTTP_PROXY")
        https_proxy = os.environ.get("HTTPS_PROXY")
        if http_proxy or https_proxy:
            proxies = {}
            if http_proxy:
                proxies["http://"] = http_proxy
            if https_proxy:
                proxies["https://"] = https_proxy
            transport = httpx.HTTPTransport(proxy=proxies)
        self.client = httpx.Client(transport=transport)

    def syncPostRequest(self) -> httpx.Response:
        return self.client.post(
            self.url,
            headers={"User-Agent": userAgent},
            json=self.data,
            timeout=self.timeout
        )

    async def asyncPostRequest(self) -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(proxy=self.client.transport.proxy)
        ) as client:
            r = await client.post(
                self.url,
                headers={"User-Agent": userAgent},
                json=self.data,
                timeout=self.timeout
            )
            return r

    def syncGetRequest(self) -> httpx.Response:
        return self.client.get(
            self.url,
            headers={"User-Agent": userAgent},
            timeout=self.timeout,
            cookies={'CONSENT': 'YES+1'}
        )

    async def asyncGetRequest(self) -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(proxy=self.client.transport.proxy)
        ) as client:
            r = await client.get(
                self.url,
                headers={"User-Agent": userAgent},
                timeout=self.timeout,
                cookies={'CONSENT': 'YES+1'}
            )
            return r
