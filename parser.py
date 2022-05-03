import requests
from bs4 import BeautifulSoup
import lxml

class Parse:
    def free_proxy_list_net():
        headers = {
            "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.9",
            "user-agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 98.0.4758.132 YaBrowser / 22.3.1.922 Yowser / 2.5 Safari / 537.36"
        }
        url = 'https://free-proxy-list.net/'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        proxy_items = soup.find('tbody').find_all('tr')
        proxy_lst = []
        for i in proxy_items:
            lst = i.getText(separator=',').split(',')
            ip_port = lst[0] + ':' + lst[1]
            lst_ready = [ip_port, lst[2], lst[4], lst[-2]]

            proxy_lst.append(lst_ready)

        print(proxy_lst)


