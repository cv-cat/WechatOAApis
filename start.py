import json
import os
import re
import time

import requests

from apis.wx_apis import WX_Apis

def norm_str(str):
    new_str = re.sub(r"|[\\/:*?\"<>| ]+", "", str).replace('\n', '').replace('\r', '')
    return new_str

def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True

if __name__ == '__main__':
    wx_apis = WX_Apis()
    cookie_str = r''
    token = r'723131708'
    querys = [
        "笛量AI",
        "帆软",
        "Convertlab"
    ]
    for query in querys:
        success, msg, res = wx_apis.get_fakeid(query, token, cookie_str)
        fakeid = res['list'][0]['fakeid']
        print(f'开始爬取{query}的所有文章')

        begin = 0
        index = 0
        while True:
            success, msg, res = wx_apis.get_shop_works(str(begin), fakeid, token, cookie_str)
            print(success, msg, res)
            time.sleep(20)
            if not success:
                if 'freq control' in msg:
                    print('请求频率过高')
                    exit(0)
                break
            for work in res["publish_list"]:
                print('=====================================')
                index += 1
                print(f'开始爬取{query}的第{index}篇文章')
                work_info = json.loads(work['publish_info'])
                link = work_info['appmsgex'][0]['link']
                mid = re.findall(r"mid=(\d+)", link)[0]
                success, msg, work_res = wx_apis.get_work_detail(link)
                time.sleep(1)
                print(success, msg, work_res)
                if success:
                    title = norm_str(work_res['title'])
                    if title.strip() == '':
                        title = f'无标题'
                    path = f'./{query}/{title}_{mid}/'
                    is_exict = check_and_create_path(path)
                    if is_exict:
                        print(f'{query}的第{index}篇文章已存在')
                        continue
                    with open(f'{path}/content.txt', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(work_res, ensure_ascii=False, separators=(',', ':')))
                    for i, image in enumerate(work_res['images']):
                        with open(f'{path}/{i}.jpg', 'wb') as f:
                            img_res = requests.get(image)
                            f.write(img_res.content)
                    print(f'{query}的第{index}篇文章完成')
                else:
                    print(f'爬取{query}的第{index}篇文章失败')

            begin += 5
            if begin > res["total_count"]:
                break



