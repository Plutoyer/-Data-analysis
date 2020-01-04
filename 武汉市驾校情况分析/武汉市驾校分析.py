# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.cluster import KMeans  # 导入K均值聚类算法
import matplotlib.pyplot as plt


# 从网页获取数据
def getText(url, d, pages):
    # 传入的三个参数分别为初始网页、数据字典、页码
    try:
        area = []
        # 驾校名称
        name = []
        # 驾校地址
        address = []
        # 价格
        price = []
        # 评分
        score = []
        # 学员数量
        stu_num = []
        # 循环遍历
        for k, v in d.items():
            for p in range(1, pages + 1):
                # 获取新的url
                new_url = url + 'wuhan/school/' + k + '/' + str(p) + 'f.html'
                # 模拟浏览器
                headers = {'User-Agent': 'Mozilla/5.0 Chrome/46.0.2490.80 '}
                print(new_url)
                # 使用requests库
                r = requests.get(new_url, headers=headers, timeout=30)
                # 状态码200
                r.raise_for_status  # 如果状态不是200，引发HTTPERROR异常
                # 设置编码格式
                r.encoding = "utf-8"
                # return r.text
                soup = BeautifulSoup(r.text, 'lxml')  # 使用lxml解析
                # print(soup)
                # 在这里用到的是beautifulsoup库
                # 定位到列表
                allinfo = soup.find('div', {'class', 'com-school-list com-part'})
                allinfo = soup.find_all('li', {'class', 'clearfix'})
                # print(allinfo)
                # 对每一个驾校的区块进行操作，获取驾校信息

                # 遍历标签li
                for info in allinfo:
                    # 驾校的名字
                    name1 = info.find_all('a', {'class': 'title'})[0].get_text()
                    # 这里使用get_text()方法获取文本 去除文本中的标签元素
                    name1 = name1.replace('\n', '').replace(' ', '')
                    # 正则表达式规范化格式
                    # 将获取的数据放入name
                    name.append(name1)
                    print(name1)

                    # 驾校的地址
                    address1 = info.find_all('p', {'class': 'field'})[0].get_text()
                    address1 = address1.replace('\n', '').replace(' ', '')
                    address.append(address1)
                    print(address1)

                    # 学员数量
                    stu_num1 = info.find_all('span', {'class': 'student'})[0].get_text()
                    stu_num1 = stu_num1.replace('\n', '').replace(' ', '').replace('名学员', '')
                    stu_num.append(stu_num1)
                    print(stu_num1)

                    # 驾校的价格
                    price1 = info.find_all('span', {'class': 'price'})[0].get_text()
                    price1 = price1.replace('￥', '').replace(' ', '').replace('面议', '')
                    price.append(price1)
                    print(price1)

                    # 驾校的评分
                    score1 = info.find_all('span', {'class': 'score'})[0].get_text()
                    score1 = score1.replace('\n', '').replace(' ', '').replace('分', '')
                    score.append(score1)
                    print(score1)
                    area.append(v)
        return area, name, address, price, score, stu_num

    except Exception as e:
        print(e)


# 存储数据
def save_data(area, name, address, price, score, stu_num):
    # pandas中的DataFrame
    result = pd.DataFrame()
    # result['v'] = v
    result['area'] = area
    result['name'] = name
    result['address'] = address
    result['price'] = price
    result['score'] = score
    result['stu_num'] = stu_num
    result.to_csv('result.csv', encoding='utf-8_sig')  # 此处的编码格式设置为utf-8_sig


# 数据处理
def clean():
    datafile = './result.csv'
    # 原始数据,第一行为属性标签
    cleanedfile = './data_cleaned.csv'
    # 数据清洗后保存的文件
    data = pd.read_csv(datafile, encoding='utf-8')
    # 读取原始数据，指定UTF-8编码
    data = data[data['price'].notnull() & data['score'].notnull()]
    # 非空值才保留
    # 只保留非零的
    index1 = data['price'] != 0
    index2 = data['score'] != 0
    index3 = data['stu_num'] != 0
    data = data[index1 | index2 | index3]  # 该规则是“或”
    data.to_csv(cleanedfile, encoding='utf-8_sig')
    # 导出结果


# 可视化
def plot():
    data = pd.read_csv('data_cleaned.csv', encoding='utf-8_sig')
    d = data['area']
    area = data['area'].drop_duplicates()
    avgp = []
    avgs = []
    avgn = []
    for a in area:
        data1 = data[data['area'] == a]
        # 平均价格取两位小数
        avgp1 = round(float(data1['price'].mean()), 2)
        avgp.append(avgp1)
        # 平均评分
        avgs1 = round(float(data1['score'].mean()), 2)
        avgs.append(avgs1)
        # 平均人数
        avgn1 = data1['stu_num'].mean()
        avgn.append(avgn1)
        # print(a,avgp1,avgs1,avgn1)
    # 求各个区平均分
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(area, avgs, color='SkyBlue')
    plt.title('武汉市各个区驾校平均评分（满分5分）')
    plt.grid(True)
    # plt.legend(lqu)
    plt.xlabel('区名')
    plt.ylabel('评分')
    plt.show()
    # 求各个区平均价格
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(area, avgp, color='SkyBlue')
    plt.title('武汉市各个区驾校平均价格')
    plt.grid(True)
    # plt.legend(lqu)
    plt.xlabel('区名')
    plt.ylabel('元')
    plt.show()
    # 求各个区平均学员数量
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(area, avgn, color='SkyBlue')
    plt.title('武汉市各个区驾校平均学员数量')
    plt.grid(True)
    # plt.legend(lqu)
    plt.xlabel('区名')
    plt.ylabel('人')
    plt.show()


# K-means聚类分析
def Kmeans():
    inputfile = './data_cleaned.csv'
    # 待聚类的数据文件
    outputfile = './fenlei.xlsx'
    k = 3
    # 需要进行的聚类类别数
    # iteration = 500
    # 聚类最大循环数
    # 读取数据并进行聚类分析
    data = pd.read_csv(inputfile)
    # 读取数据
    data = data[['price', 'score', 'stu_num']]
    # 调用k-means算法，进行聚类分析
    kmodel = KMeans(n_clusters=k, n_jobs=4)
    # n_jobs是并行数，一般等于CPU数较好
    kmodel.fit(data)
    # 训练模型
    r1 = pd.Series(kmodel.labels_).value_counts()
    # 统计各个类别的数目
    r2 = pd.DataFrame(kmodel.cluster_centers_)
    # 找出聚类中心
    r = pd.concat([r2, r1], axis=1)
    # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
    r.columns = list(data.columns) + [u'类别数目']
    # 重命名表头
    print("聚类表结果：")
    print(r)

    r = pd.concat([data, pd.Series(kmodel.labels_, index=data.index)], axis=1)
    # 详细输出每个样本对应的类别
    r.columns = list(data.columns) + [u'聚类类别']
    # 重命名表头
    r.to_excel(outputfile)
    # 保存分类结果
    print("聚类图结果：")
    p = data.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    [p[i].set_ylabel('density') for i in range(k)]
    plt.legend()
    # pic_output = 'D://mypy/' #概率密度图文件名前缀
    # for i in range(k):
    #     density_plot(data[r[u'聚类类别']==i]).savefig(u'%s%s.png' %(pic_output, i))


# 主任务
def run():
    # url
    first_url = "http://www.jiakaobaodian.com/"
    # d可自由设定 需要理解key和value
    d = {'q_jiangan0': '江岸区', 'q_jianghan': '江汉区', 'q_qiaokou': '硚口区', 'q_hanyang': '汉阳区', 'q_wuchang': '武昌区',
         'q_qingshan': '青山区', 'q_hongshan1': '洪山区','q_dongxihu': '东西湖区','q_hannan': '汉南区' ,'q_caidian0': '蔡甸区', 'q_jiangxia': '江夏区', 'q_huangpi': '黄陂区','q_xinzhou0': '新洲区'}
    # 调用def
    # 获取数据
    area, name, address, price, score, stu_num = getText(first_url, d, 4)
    # 存储数据
    save_data(area, name, address, price, score, stu_num)
    # 数据清洗
    clean()
    # 绘图
    plot()
    # 聚类分析
    Kmeans()


# 执行
if __name__ == '__main__':
    run()
    # fillUnivList(html)