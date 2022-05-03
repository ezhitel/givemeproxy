from db_handler import GiveMeProxy_DB
from parser import Parse


class GiveMeProxy:
    def __init__(self,
                 proxy_type='any',
                 country='all',
                 anonymity='any',
                 refresh_time=10,
                 proxy_check=True,
                 ):

        self.proxy_type = ''
        self.country = ''
        self.anonymity = ''
        self.proxy_check = True

        self.check_param(proxy_type,
                         country,
                         anonymity,
                         refresh_time,
                         proxy_check
                         )

        self.current_proxy_id = 0
        self.proxys = []
        self.current_proxy = ''
        self.blocked_list = []
        self.db = GiveMeProxy_DB(refresh_time)
        self.parse = Parse()
        self.get_proxy  # get list of proxy ids

    def check_param(self,
                    proxy_type,
                    country,
                    anonymity,
                    refresh_time,
                    proxy_check,
                    ):
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

        # Check proxy_type type and value
        if type(proxy_type) == str:
            for i in proxy_type:
                if i in proxy_type_list:
                    continue
                else:
                    raise ValueError(
                        'Incorrect proxy_type value specified. Use: "any", "socks4", "socks5", "http", "https".')
            self.proxy_type = proxy_type
        else:
            raise TypeError('Incorrect proxy_type type specified. Expected string.')

        # Check country type and value
        if type(country) == str:
            for i in country:
                if i in coutry_code_list:
                    continue
                else:
                    raise ValueError('Incorrect country value specified. Use ISO 3166-1 alpha-2 codes.')
            self.country = country
        else:
            raise TypeError('Incorrect country type specified. Expected string.')

        # Check anonymity type and value
        if type(anonymity) == str:
            for i in anonymity:
                if i in anonymity_list:
                    continue
                else:
                    raise ValueError('Incorrect anonymity value specified. Use: "any", "elite", "anon", "transparent".')
            self.anonymity = anonymity
        else:
            raise TypeError('Incorrect anonymity type specified. Expected string.')

        # Check refresh_time type
        if type(refresh_time) == int:
            pass
        else:
            raise TypeError('Incorrect refresh_time type specified. Expected integer.')

        # Check proxy_check type
        if type(proxy_check) == bool:
            self.proxy_check = proxy_check
        else:
            raise TypeError('Incorrect proxy_check type specified. Expected bool.')

    def force_parse(self):
        self.parse.now()


    def get_proxy(self):
        for i in range(2):
            data = self.db.get_info(self.proxy_type, self.country, self.anonymity, self.proxy_check)
            if data is not False:
                self.proxys = list(data)
                return True
            elif i != 1:
                self.force_parse()

    raise RuntimeError('No suitable proxies found')


def this(self):
    for i in range(2):
        if self.current_proxy != '':
            return self.current_proxy
        elif i != 1:
            _next()


def _next(self):
    for i in range(2):
        if self.proxys:
            proxys_len = len(self.proxys)
            for i in proxys_len:
                candidate = self.proxys.pop(0)
                if is_not_blocked(candidate):
                    self.current_proxy = candidate
                    return self.current_proxy
        elif i != 1:
            self.get_proxy
    raise RuntimeError('No suitable proxies found')


def block(self, ip='current_ip'):
    if ip == 'current_ip':
        self.blocked_list.append(self.current_proxy)
    else:
        self.blocked_list.append(ip)


def is_not_blocked(self, ip):
    if ip not in self.blocked_list:
        return True
    else:
        return False
