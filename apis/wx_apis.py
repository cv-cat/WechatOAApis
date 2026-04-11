import re
import bs4
import time
import json
import requests
from bs4 import BeautifulSoup
from functools import partial
from utils.wx_utils import get_common_headers, get_fakeid_params, trans_cookies, get_shop_works_params, text_contains

class WX_Apis():

    """
        获取公众号的id
        :param query: 公众号名称
        :param token: token
        :param cookies_str: cookies字符串
        返回公众号的id
    """
    def get_fakeid(self, query: str, token: str, cookies_str: str, proxies: dict = None):
        success = True
        res_json = None
        msg = '成功'
        try:
            url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
            headers = get_common_headers()
            params = get_fakeid_params(query, token)
            cookies = trans_cookies(cookies_str)
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            res_json = response.json()
            if res_json["base_resp"]["ret"] != 0:
                msg = res_json["base_resp"]["err_msg"]
                success = False
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取公众号的文章
        :param begin: 开始位置
        :param fakeid: 公众号id
        :param token: token
        :param cookies_str: cookies字符串
        返回公众号的文章
    """
    def get_shop_works(self, begin: str, fakeid: str, token: str, cookies_str: str, proxies: dict = None):
        success = True
        res = None
        msg = '成功'
        try:
            url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
            headers = get_common_headers()
            params = get_shop_works_params(begin, fakeid, token)
            cookies = trans_cookies(cookies_str)
            response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxies)
            res_json = response.json()
            if res_json["base_resp"]["ret"] != 0:
                msg = res_json["base_resp"]["err_msg"]
                success = False
            else:
                res = res_json["publish_page"]
                res = json.loads(res)
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

    """
        获取公众号的所有文章
        :param fakeid: 公众号id
        :param token: token
        :param cookies_str: cookies字符串
        返回公众号的所有文章
    """
    def get_shop_all_works(self, fakeid: str, token: str, cookies_str: str, sleep_time: int = 0, proxies: dict = None):
        success = True
        msg = '成功'
        works = []
        try:
            begin = 0
            while True:
                success, msg, res = self.get_shop_works(str(begin), fakeid, token, cookies_str, proxies)
                if not success:
                    break
                works.extend(res["publish_list"])
                time.sleep(sleep_time)
                begin += 5
                if begin > res["total_count"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, works

    """
        获取文章的内容
        :param url
        获取文章的内容
    """
    def get_work_detail(self, url: str):
        success = True
        msg = '成功'
        res = None
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'lxml')
            title = soup.find('meta', attrs={'property': 'og:title'})['content']
            author = soup.find('meta', attrs={'property': 'og:article:author'})['content']
            profile = soup.find('strong', attrs={'class': 'profile_nickname'}).text
            js_content = soup.find('div', attrs={'id': 'js_content'})
            images = []
            for img in js_content.find_all('img'):
                images.append(img['data-src'])
            all_contents = []
            for child in js_content.descendants:
                if type(child) == bs4.element.NavigableString:
                    all_contents.append(child.get_text())
            joined_content = "\n".join(all_contents)
            scripts = soup.find(partial(text_contains, substr="window.cgiData", tag_name="script")).text
            city_str = re.findall(r"provinceName: '(.*?)'", scripts)
            if city_str:
                city = city_str[0]
            else:
                city = None
            scripts2 = soup.find(partial(text_contains, substr="function __setPubTime", tag_name="script")).text
            time_str = re.findall(r"createTime = '(.*?)'", scripts2)
            if time_str:
                time = time_str[0]
            else:
                time = None
            res = {
                "source_platform": "wx",
                "url": url,
                "title": title,
                "content": joined_content,
                "images": images,
                "author": {
                    "user": author,  # 作者昵称
                    "profile": profile,  # 公众号名字
                    "city": city
                },
                "time": time
            }
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res

if __name__ == '__main__':
    # 获取公众号所有文章需要cookie和token信息，而fakeid是公众号的唯一标识，通过搜索公众号接口获取
    # freq control是请求频率
    wx_apis = WX_Apis()
    token = r''
    cookie_str = r''
    token = r'1638551384'
    query = "麦麦Studio"
    # 获取公众号的id
    success, msg, res = wx_apis.get_fakeid(query, token, cookie_str)
    print(success, msg, res)
    shop_id = res['list'][0]['fakeid']
    # 获取公众号的所有文章
    success, msg, res = wx_apis.get_shop_all_works(shop_id, token, cookie_str)
    print(success, msg, res)
    print(success, msg, json.dumps(res, ensure_ascii=False, separators=(',', ':')))
    print(len(res))
    print(json.dumps(json.loads(res[2]['publish_info']), ensure_ascii=False, separators=(',', ':')))
    # 获取文章的内容
    # url = "https://mp.weixin.qq.com/s?__biz=MzU1MDk0ODI4Mw==&mid=2247510137&idx=3&sn=c65cf661a4f9516fde7bc79a97ebe79d&chksm=fb9a34adccedbdbb03ca2d3dd58d6320fdf8ea9d89af01ca383b613fc4270b350e457e0bed20#rd"
    # success, msg, res = wx_apis.get_work_detail(url)
    # print(success, msg, res)
    # print(success, msg, json.dumps(res, ensure_ascii=False, separators=(',', ':')))

