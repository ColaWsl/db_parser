import csv
import random
import requests
from bs4 import BeautifulSoup


# 随机生成浏览器标识 user agent
def get_user_agent():
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    user_agent = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                           '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                          )
    return user_agent


# 获取快代理免费的高密IP
def get_ipinfo(soup, str_craw, key, value):
    a = soup.find(str_craw, attrs={key: value}).text
    return a


# 抓取快代理第一页：类型，IP地址，
ip_info = []

for i in range(2, 3):  # 前1页
    url = r"https://www.kuaidaili.com/free/inha/{}".format(i)
    headers = {
        'User-Agent': get_user_agent()
    }

    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, features='lxml')

    link_table = soup.find('tbody')

    for tr_data in link_table.find_all('tr'):
        dic = {}
        ip = str(get_ipinfo(tr_data, 'td', 'data-title', 'IP'))
        http = str(get_ipinfo(tr_data, 'td', 'data-title', '类型'))
        dic[http] = ip
        ip_info.append(dic)

print(ip_info)


class DoubanParser:
    book_dict = {}

    def parse(self, page_url):

        for num in range(0, 40, 20):
            headers = {'User-Agent': get_user_agent()}
            proxy = random.choice(ip_info)
            url = page_url + '?start=' + num.__str__()
            res = requests.get(url=url, headers=headers, proxies=proxy)

            page_soup = BeautifulSoup(res.text, 'lxml')
            book_titles = page_soup.find_all('div', {'class': 'info'})

            cnt = 0
            for title in book_titles:
                cnt = cnt + 1
                book_link = title.h2.a
                title = book_link.get_text().replace(" ", "").replace("\n", "")
                link = book_link["href"]
                description = self.get_book_description(link)
                print(f'{title}:{link}')
                self.book_dict[title] = description
                if cnt == 20:
                    break

    def get_book_description(self, page_url):
        headers = {'User-Agent': get_user_agent()}
        proxy = random.choice(ip_info)
        res = requests.get(url=page_url, headers=headers, proxies=proxy)

        page_soup = BeautifulSoup(res.text, features='lxml')

        description = page_soup.find('div', {'class': 'intro'})
        text = description.get_text()
        return text

    def write_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(['book_title', 'description'])
            for title, description in self.book_dict.items():
                write.writerow([title, description])


doubanParser = DoubanParser()
new_page = 'https://book.douban.com/tag/%E7%BC%96%E7%A8%8B'
doubanParser.parse(new_page)
doubanParser.write_to_csv('book.csv')
