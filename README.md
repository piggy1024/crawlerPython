# crawlerPython

#### 介绍
使用python根据指定数据源找到其ajax请求的的股票数据,爬取出指定格式的数据,并存储到数据库或者导出csv到文件

#### 整体结构
 class Stock_Spider(object):
      # 初始化函数
      def __init__(self):

      # 数据库连接函数
      def connect(self):

      # 数据存储进数据库
      def save_data(self):

      # 拼接url(大宗交易的url)
      def get_url_list_dzjy(self):

      # 发送请求
      def send_request(self, url):

      # 获取起始交易日start_time
      def get_start_time(self):

      # 获取所有对应股票代码code的函数
      def get_all_codes(self):

      # 1下载历史交易数据函数
      def download_lsjysj(self):

      # 2 处理获取资金流向的数据
      def get_zjlx_data(self):

      # 3 处理获取大宗交易的数据
      def get_dzjy_data(self):

      # 4 处理融资融券的数据
      def get_rzrq_data(self):

      # 统一调度
      def start(self):

Stock_Spider().start()

