import csv
import requests
import random
from util import agent
from util import ipproxy
from bs4 import BeautifulSoup


class DoubanParser:
    book_dict = {}

    def parse(self, page_url):

        for num in range(0, 40, 20):
            headers = {'User-Agent': agent.get()}
            proxy = random.choice(ipproxy.get_ips())
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
        headers = {'User-Agent': agent.get()}
        proxy = random.choice(ipproxy.get_ips())
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
