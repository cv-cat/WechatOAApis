import json
import os
import re

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
        # "笛量AI",
        # "帆软",
        "ConvertlaC"
    ]
    for query in querys:
        success, msg, res = wx_apis.get_fakeid(query, token, cookie_str)
        shop_id = res['list'][0]['fakeid']
        print(f'开始爬取{query}的所有文章')
        success, msg, res = wx_apis.get_shop_all_works(shop_id, token, cookie_str, sleep_time=20)
        print(f'获取到{query}的{len(res)}篇文章')
        for index, work in enumerate(res):
            print(f'开始爬取{query}的第{index + 1}篇文章')
            work_info = json.loads(work['publish_info'])
            link = work_info['appmsgex'][0]['link']
            mid = re.findall(r"mid=(\d+)", link)[0]
            success, msg, work_res = wx_apis.get_work_detail(link)
            if success:
                title = norm_str(work_res['title'])
                if title.strip() == '':
                    title = f'无标题'
                path = f'./{query}/{title}_{mid}/'
                isExist = check_and_create_path(path)


                # 打开这个注释，相当于只获取最新的文章，注释掉这个，相当于获取所有文章
                # if isExist:
                #     break


                with open(f'{path}/content.html', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(work_res, ensure_ascii=False, separators=(',', ':')))
                for i, image in enumerate(work_res['images']):
                    with open(f'{path}/{i}.jpg', 'wb') as f:
                        img_res = requests.get(image)
                        f.write(img_res.content)
                print(f'{query}的第{index + 1}篇文章完成')
            else:
                print(f'爬取{query}的第{index + 1}篇文章失败')
            print('=====================================')
        print(f'爬取{query}的所有文章完成')

