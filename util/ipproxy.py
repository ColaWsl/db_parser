import requests
from bs4 import BeautifulSoup
from util import agent


# 获取快代理免费的高密IP
def get_ipinfo(soup, str_craw, key, value):
    a = soup.find(str_craw, attrs={key: value}).text
    return a


# 抓取快代理第一页：类型，IP地址，
def get_ips():
    ips = []
    for i in range(2, 3):  # 前1页
        url = r"https://www.kuaidaili.com/free/inha/{}".format(i)
        headers = {
            'User-Agent': agent.get()
        }

        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, features='lxml')

        link_table = soup.find('tbody')

        for tr_data in link_table.find_all('tr'):
            dic = {}
            ip = str(get_ipinfo(tr_data, 'td', 'data-title', 'IP'))
            http = str(get_ipinfo(tr_data, 'td', 'data-title', '类型'))
            dic[http] = ip
            ips.append(dic)

    return ips
