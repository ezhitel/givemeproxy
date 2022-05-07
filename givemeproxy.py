from main import Main
import asyncio


class GiveMeProxy(Main):
    def __init__(self,
                 proxy_type: str = 'any',
                 country: str = 'all',
                 anonymity: str = 'any',
                 refresh_time: int = 10,
                 proxy_check: bool = False,
                 ):


        super().__init__(proxy_type, country, anonymity, refresh_time, proxy_check)



    def force_parse(self):
        asyncio.run(self.start_parse())

    def this(self):
        return self.current_proxy

    def _next(self):
        return self.next_from_queue()

    def block(self, ip: str = 'current'):
        if ip == 'current':
         self.blocked_list.append(self.current_proxy)
        else:
            self.blocked_list.append(ip)

    def all(self):
        return list(self.suitable_proxies)
