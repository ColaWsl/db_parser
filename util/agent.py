import random


# 随机生成浏览器标识 user agent
def get():
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
