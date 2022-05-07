from bs4 import BeautifulSoup
import aiohttp
import asyncio
from collections import deque


class Parse:
    def __init__(self):
        self.parse_in_progress = False
        self.headers = {
            "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.9",
            "user-agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 98.0.4758.132 YaBrowser / 22.3.1.922 Yowser / 2.5 Safari / 537.36"
        }

    async def free_proxy_list_net(self, queue, parse_defs_done):
        url = 'https://free-proxy-list.net/'
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=url) as response:
                site_data = await response.text()
        soup = BeautifulSoup(site_data, 'lxml')
        proxy_items = soup.find('tbody').find_all('tr')

        for i in proxy_items:
            lst = i.getText(separator=',').split(',')
            ip_port = lst[0] + ':' + lst[1]
            if 'elite' in lst[4]:
                anon = 'elite'
            else:
                anon = lst[4]
            lst_ready = [ip_port, lst[2], anon, lst[-2]]
            await queue.put(lst_ready)
        await parse_defs_done.put('free_proxy_list_net')


