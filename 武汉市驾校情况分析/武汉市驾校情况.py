import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


# 代码框架
def getText(url, d, pages):
    try:
        name = []
        address = []
        price = []
        score = []
        stu_num = []
        for k, v in d.items():
            for p in range(1, pages + 1):
                new_url = url + k + '/school' + '/' + str(p) + 'f.html'
                headers = {'User-Agent': 'Mozilla/5.0 Chrome/46.0.2490.80 '}
                print(new_url)
                r = requests.get(new_url, headers=headers, timeout=30)
                r.raise_for_status  # 如果状态不是200，引发HTTPERROR异常
                r.encoding = "utf-8"
                # return r.text
                soup = BeautifulSoup(r.text, 'lxml')
                # print(soup)
                allinfo = soup.find('div', {'class', 'com-school-list com-part'})
                allinfo = soup.find_all('li', {'class', 'clearfix'})
                # print(allinfo)
                # 对每一个驾校的区块进行操作，获取驾校信息

                for info in allinfo:
                    # 驾校的名字
                    name1 = info.find_all('a', {'class': 'title'})[0].get_text()
                    name1 = name1.replace('\n', '').replace(' ', '')
                    name.append(name1)
                    print(name1)
                    # 驾校的地址
                    address1 = info.find_all('p', {'class': 'field'})[0].get_text()
                    address1 = address1.replace('\n', '').replace(' ', '')
                    address.append(address1)
                    print(address1)

                    # 学员数量
                    stu_num1 = info.find_all('span', {'class': 'student'})[0].get_text()
                    stu_num1 = stu_num1.replace('\n', '').replace(' ', '')
                    stu_num.append(stu_num1)
                    print(stu_num1)
                    # 驾校的价格
                    price1 = info.find_all('span', {'class': 'price'})[0].get_text()
                    price1 == price1.replace('\n', '').replace(' ', '')
                    price.append(price1)
                    print(price1)

                    # 驾校的评分
                    score1 = info.find_all('span', {'class': 'score'})[0].get_text()
                    score1 == score1.replace('\n', '').replace(' ', '')
                    score.append(score1)
                    print(score1)
        return name, address, price, score, stu_num

    except Exception as e:
        print(e)


# 存储数据
def save_data(name, address, price, score, stu_num):
    result = pd.DataFrame()
    # result['v'] = v
    result['name'] = name
    result['address'] = address
    result['price'] = price
    result['score'] = score
    result['stu_num'] = stu_num
    result.to_csv('result.csv', encoding='utf-8_sig')


# 主任务
def run():
    first_url = "http://www.jiakaobaodian.com/"
    d = {'wuhan': '武汉市'}
    name, address, price, score, stu_num = getText(first_url, d, 4)
    save_data(name, address, price, score, stu_num)


# 执行
if __name__ == '__main__':
    run()
    # fillUnivList(html)