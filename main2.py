import requests
import base64
import json
import os

from messenger import Messenger


import time

headers_1 = {
        "Cookie": "arccount62298=c; arccount62019=c",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
    } # 验证码token爬取

headers_2 = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "fangkong.hnu.edu.cn",
        "Origin": "https://fangkong.hnu.edu.cn",
        "Referer": "https://fangkong.hnu.edu.cn/app/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"
    } # 登录及打卡

headers_3 = {
        'Host': 'cloud.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
        'Accept': '*/*',
        'Origin': 'https://cloud.baidu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cloud.baidu.com/product/ocr/general',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    } # 百度OCR识别验证码

# 获取变量
users_data = os.getenv("users_data")
sckey = os.getenv("sckey")

# step 1: 获取验证码Token及图片

def ClockIn(user_data,messenger):
    try:
        token_json = requests.get("https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode", headers=headers_1)

        if token_json.status_code!=200: print("Token爬取失败，正在重试")
        while (token_json.status_code!=200):
            token_json = requests.get("https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode", headers=headers_1)

        data = json.loads(token_json.text)
        token = data["data"]["Token"]
        
        img_url = "https://fangkong.hnu.edu.cn/imagevcode?token=" + token
        with open("img.jpg", "wb") as img:
            img.write(requests.get(img_url).content)

        
        # 解析验证码

        with open("img.jpg",'rb') as f:
            img = base64.b64encode(f.read())
        data = {
            'image': 'data:image/jpeg;base64,'+str(img)[2:-1],
            'image_url': '',
            'type': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
            'detect_direction': 'false'
        }

        response = requests.post('https://cloud.baidu.com/aidemo', headers=headers_3, data=data)
        result = response.json()['data']['words_result'][0]['words']

        # step 2: 模拟登录操作

        data = {
            "Code": user_data['usr'],
            "Password": user_data['pwd'],
            "Token": token,
            "VerCode": result
        }

        session = requests.Session()
        response = session.post("https://fangkong.hnu.edu.cn/api/v1/account/login", headers=headers_2, data=json.dumps(data))

        if response.json()["code"] != 0:
            print("验证码错误")
            ClockIn()
        else:
            if user_data['usr'][0] == 'S':
                data2 = {
                    "BackState": 1,
                    "MorningTemp": "36.5",
                    "NightTemp": "36.5",
                    "RealAddress": "芙蓉国际",
                    "RealCity": "常德市",
                    "RealCounty": "武陵区",
                    "RealProvince": "湖南省",
                    "tripinfolist": []
                }
            else:
                data2 = {
                    "BackState": 1,
                    "MorningTemp": "36.5",
                    "NightTemp": "36.5",
                    "RealAddress": "湖南大学",
                    "RealCity": "长沙市",
                    "RealCounty": "岳麓区",
                    "RealProvince": "湖南省",
                    "tripinfolist": []
                }

            response = session.post("https://fangkong.hnu.edu.cn/api/v1/clockinlog/add", headers=headers_2, data=json.dumps(data2))

            msg = response.json()["msg"]
            messenger.send(text= user_data['usr'] + msg )
    except:
        print("Error")
        messenger.send(text = '打卡失败,请手动打卡啊')
        ClockIn(user_data,messenger)

if __name__ == '__main__':

    messenger = Messenger(sc_key=sckey)

    for user_data in eval(users_data):
        ClockIn(user_data,messenger)
        time.sleep(2)

