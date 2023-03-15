import re
import json
import requests
from lxml import etree


class csdn:
    url = 'https://www.csdn.net/'

    XPATH_TITLE = '//span[@class="blog-text"]/text()'
    XPATH_BODY = '//p[@class="desc"]/text()'

    proxies = {
        'http': '127.0.0.1:7890',
        'https': '127.0.0.1:7890'
    }

    headers = {
        # 'Cookie':'uuid_tt_dd=10_36834004830-1622022679287-812113; log_Id_pv=8677; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1678442902,1678668001,1678865411,1678890334; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22qq_53872312%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_36834004…Tac75Lo3ruX-et38f53Hy9M10GXSFtEscmTKvl1yeCOutuma7A%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; acw_tc=2760829916788903266438890e9e5e7ae078821bf872da602b7d4453f47370; dc_session_id=10_1678890326667.997949; csrfToken=Cdd7ctXvqTv_Jk_Ugis1hB1p; c_pref=default; c_ref=default; c_dsid=11_1678890332426.920640; c_first_ref=default; c_first_page=https%3A//www.csdn.net/; c_segment=1; c_page_id=default; dc_tos=rrkg2k; www_red_day_last=red; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1678890334; dc_sid=6670d2874b261147d928a26e41441fd1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
    }

    def save_html(self, html):
        """
        用于保存爬取的html信息
        :param html: 网页内容
        :return: None
        """
        with open('data/csdn.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def sig_in(self):
        """
        进入csdn获取网页信息
        :return: html
        """
        with requests.get(url=self.url, headers=self.headers, proxies=self.proxies) as response:
            response.encoding = 'utf-8'
            context = response.text
        return context

    def apparatus(self, html=None):
        """
        用于解析网页对象
        :param html: 网页对象
        :return: data
        """
        if html is None:
            with open('data/csdn.html', 'r', encoding='utf-8') as f:
                html = f.read()
        tree = etree.HTML(html)

        titles = tree.xpath(self.XPATH_TITLE)
        bodies = tree.xpath(self.XPATH_BODY)

        data = {title: body for title, body in zip(titles, bodies)}
        return data

    def save_data(self, data):
        """
        用于保存解析后的信息
        :param data: data
        :return: None
        """
        with open('data/blog.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def __init__(self):
        pass


if __name__ == '__main__':
    object = csdn()

    html = object.sig_in()  # 爬取

    object.save_html(html)  # 保存网页

    data = object.apparatus()  # 提取解析

    object.save_data(data)  # 保存信息
