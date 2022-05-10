from collections import deque

from parser import Parse
from db_handler import GiveMeProxy_DB
import asyncio
parse = Parse()
db = GiveMeProxy_DB()
class Main():
    def __init__(self, proxy_type, country, anonymity):
        self.proxy_type = ''
        self.country = ''
        self.anonymity = ''

        self.check_param(proxy_type,
                         country,
                         anonymity
                         )
        self.current_proxy = ''
        self.current_proxy_protocol = ''
        self.blocked_list = []
        self.suitable_proxies = deque()
        self.append_suitable_proxies()

    def check_param(self, proxy_type, country, anonymity):
        proxy_type_list = ['any', 'socks4', 'socks5', 'http', 'https']
        coutry_code_list = ['all', 'AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU',
                            'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA',
                            'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD',
                            'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY',
                            'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ',
                            'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP',
                            'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID',
                            'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR',
                            'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW',
                            'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME',
                            'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF',
                            'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR',
                            'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST',
                            'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES',
                            'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK',
                            'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ',
                            'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']
        anonymity_list = ['any', 'elite', 'anon', 'transparent']

        # Check proxy_type value
        for i in proxy_type:
            if i in proxy_type_list:
                break
            else:
                raise ValueError(
                    'Incorrect proxy_type value specified. Use: "any", "socks4", "socks5", "http", "https".')
        self.proxy_type = proxy_type

        # Check country value
        for i in country:
            if i in coutry_code_list:
                break
            else:
                raise ValueError('Incorrect country value specified. Use ISO 3166-1 alpha-2 codes.')
        self.country = country


        # Check anonymity value
        for i in anonymity:
            if i in anonymity_list:
                break
            else:
                raise ValueError('Incorrect anonymity value specified. Use: "any", "elite", "anon", "transparent".')
        self.anonymity = anonymity

    def append_suitable_proxies(self):
        for i in range(2):
            data = db.get_data(self.proxy_type, self.country, self.anonymity)
            if data:
                for x in data:
                    if self.is_not_blocked(x[0]):
                        self.suitable_proxies.append(x)
                if self.suitable_proxies:
                    return True
                else:
                    raise RuntimeError('No suitable proxies found')
            elif i != 1:
                asyncio.run(self.start_parse())

        raise RuntimeError('No suitable proxies found')

    async def start_parse(self):
        queue = asyncio.Queue()
        parse_defs_done = asyncio.Queue(maxsize=1)
        await asyncio.gather(self.insert_to_db(queue, parse_defs_done),
                             parse.free_proxy_list_net(queue, parse_defs_done),
                             )


    async def insert_to_db(self, queue, parse_defs_done):
        #db.drop_table()
        await asyncio.sleep(0.1)
        while not parse_defs_done.full():
            await asyncio.sleep(0.1)
            while not queue.empty():
                data = await queue.get()
                #db.insert(data)
                print(data)


    def next_from_queue(self):
        # TODO: Проверить что возвращает очередь если пуста
        data_from_queue = self.suitable_proxies.popleft()
        try:
            self.current_proxy = data_from_queue[0]
            self.current_proxy_protocol = data_from_queue[1]
        except:
            asyncio.run(self.start_parse())
            self.append_suitable_proxies()
            data_from_queue = self.suitable_proxies.popleft()
            self.current_proxy = data_from_queue[0]
            self.current_proxy_protocol = data_from_queue[1]
        finally:
            return self.current_proxy


    def is_not_blocked(self, ip):
        if ip not in self.blocked_list:
            return True
        else:
            return False

main = Main(proxy_type=['any'], country=['all'], anonymity=['any'], refresh_time=10)

asyncio.run(main.start_parse())