# -*- coding:utf8 -*-
import random
import re
import requests
from lxml import etree



class Stock_Spider(object):
    def __init__(self):
        # all_code_url
        self.all_code_url = 'http://quote.eastmoney.com/stock_list.html'
        # 需要的 60 30 00开头的代码
        self.need_codes = []
        self.test =[]


        # 网址切成前后两节,重建拼接code(大宗交易的url)
        self.base_url_q ='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=TDATE&sr=-1&p=1&ps=50&filter=(SECUCODE=%27'
        self.base_url_h ='%27)&js=var%20TGyGbAqk={pages:(tp),data:(x)}&type=DZJYXQ&rt=52774321'

        # 请求头的添加
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0']
        ua = random.choice(ua_list)
        self.headers = {'User-Agent':ua}


    # 拼接url(大宗交易的url)
    def get_url_list(self):
        # 存放拼接好的url的列表
        url_list = []
        for code in self.need_codes:
            url1 = self.base_url_q + code + self.base_url_h
            url_list.append(url1)
        # print(url_list)
        return url_list


    # 发送请求
    def send_request(self, url):
        # data = requests.get(url, headers=self.headers).content.decode()
        response = requests.get(url, headers=self.headers)
        # response.encoding = 'gbk'
        data = response.text
        # print(data)

        return data

    # 解析数据
    def parse_xpath_data(self, data):
        pass

    # 获取起始交易日start_time
    def get_start_time(self):
        url = 'http://quotes.money.163.com/trade/lsjysj_000001.html'
        data = self.send_request(url)
        html = etree.HTML(data)
        start_times = html.xpath('/html/body/div[2]/div[5]/div[2]/form/table[2]/tbody/tr[1]/td[2]/input[3]/@value')
        print(start_times[0])

    # 获取所有code的函数
    def get_all_codes(self):

        # 1发起得到所有code的请求
        data1 = self.send_request(self.all_code_url)
        html = etree.HTML(data1)
        # print(html)
        all_codes = html.xpath('//*[@id="quotesearch"]//ul//li//a//text()')

        # 将所有的股票代码信息存储到表sraw_stock_list
        # for code in all_codes:
        #     insert_data = {
        #         'code':code
        #     }
        #     cursor.execute(sql_insert_sraw_code, insert_data)
        #     conn.commit()

        # 保存60,30及00开头的数据到表stock_list
        for code in all_codes:
            # 利用正则获取60 00 30 开头的code
            pattern = re.compile(r'[(]([60|00|30]+\d{4})[)]', re.S)
            x = pattern.findall(code)

            #     # 上面得到的列表x有些是空的(不符合60\00\30那些)
            if (len(x) > 0):
                code_number = x[0]
                # 放进列表self.need_codes
                self.need_codes.append(x[0])

                # 插入数据的操作
                insert_data = {
                    'code_number': code_number
                }
                # cursor.execute(sql_insert_code, insert_data)
                # conn.commit()
        # print(self.need_codes)

    # 处理大宗交易的数据
    def get_dzjy_data(self):
        # 调用拼接url函数 获取 要请求的url(大宗交易)
        url_list = self.get_url_list()

        for url in url_list[0:10]:
            response = requests.get(url,headers = self.headers)
            data = response.text

            # 使用正则取出data[]里的内容
            pattern = re.compile('[[](.*?)[]]', re.S)
            all_new_data = pattern.findall(data)
            # print(all_new_data[0]) # {"TDATE":"2020-02-27T00:00:00","SECUCODE":"600000","SNAME":"浦发银行","PRICE":11.21},{"TDATE":"2020-02-27T00:00:00","SECUCODE":"600000","SNAME":"浦发银行","PRICE":11.21}

            for new_data in all_new_data:
                pattern1 = re.compile(r'[{](.*?)[}]')
                # x是列表 包含了每一天的数据
                x = pattern1.findall(new_data)
                # print(x) #['"TDATE":"2020-02-27T00:00:00","SECUCODE":"600000","SNAME":"浦发银行","PRICE":11.21,"TVOL":29.5,"TVAL":330.7"','"TDATE":"2020-02-27T00:00:00","SECUCODE":"600000","SNAME":"浦发银行","PRICE":11.21,"TVOL":29.5,"TVAL":330.7"']
                # x[0]  = "TDATE":"2020-02-27T00:00:00","SECUCODE":"600000","SNAME":"浦发银行","PRICE":11.21

                # 分割函数获取每个key:value获取键值对
                for detail in x:
                    details = detail.split(",")
                    # print(details)   # ['"TDATE":"2020-02-27T00:00:00"', '"SECUCODE":"600000"']

                # 正则匹配 key value 的值 获取数字数据
                # 匹配小数
                pattern = re.compile(r'[0-9]*\.?[0-9]+', re.S)
                i = 0
                for new_data1 in details:

                    new_datas = pattern.findall(new_data1)  # detail[0]="TDATE":"2020-02-27T00:00:00"

                    # print(new_datas) # ['TDATE', '2020-02-27T00:00:00']
                    if i == 3:
                        final_price = new_datas[0]
                        print('成交价:',final_price)
                    if i == 4:
                        volume = new_datas[0]
                        print('成交量:',volume)
                    if i == 5:
                        turnover_amount = new_datas[0]
                        print('成交额:',turnover_amount)
                    if i == 12:
                        raise_and_fall = new_datas[0] # 负号没取到
                        print('涨跌幅:',raise_and_fall)
                    if i == 13:
                        close_price = new_datas[0]
                        print('收盘价:',close_price)
                    if i == 15:
                        floding_rate = new_datas[0]
                        print('折溢率:',floding_rate)
                    if i == 16:
                        market_value = new_datas[0]
                        print('流通市值:',market_value)
                    if i == 17:
                        ups_and_downs = new_datas[1]
                        print('上榜后涨跌幅:',ups_and_downs)

                    i += 1

                # 正则匹配 key value 的值 ""获取""包括数据
                # 匹配""内的数据
                j = 0
                pattern = re.compile(r'["](.*?)["]+', re.S)
                for new_data2 in details:
                    new_datas = pattern.findall(new_data2)
                    # print(new_datas)
                    if j == 0:
                        trade_date = new_datas[1]
                        print('交易日期:',trade_date)
                    if j == 7:
                        buyer_department = new_datas[1]
                        print('买方营业部:',buyer_department)
                    if j == 9:
                        seller_department = new_datas[1]
                        print('卖方营业部:',seller_department)

                    j += 1


    # 统一调度
    def start(self):

        # 调用获取codes
        self.get_all_codes()

        # 调用获取起始日期的函数
        self.get_start_time()


        # 调用大宗交易数据获取函数
        self.get_dzjy_data()







Stock_Spider().start()