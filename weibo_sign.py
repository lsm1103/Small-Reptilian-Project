import re
import time
import json
import requests
import base64
import binascii
import re
from urllib import parse
from fake_useragent import UserAgent
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5


class WeiboLogin(object):
    """docstring for WeiboLogin"""
    def __init__(self, username, password):
        super(WeiboLogin, self).__init__()
        self.username = username
        self.password = password
        session = requests.session()
        ua = UserAgent()
        session.headers['User-Agent'] = ua.random
        self.session = session
        # session.headers.update({
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
        # })

    def get_pubkey(self):
        # 1.请求首页面
        self.session.get('https://weibo.com')
        # 2.请求pre_login 获取参数
        params = {
                    'entry': 'weibo',
                    'callback': 'sinaSSOController.preloginCallBack',
                    'su': '',
                    'rsakt': 'mod',
                    'client': 'ssologin.js(v1.4.19)',
                    '_': int(time.time())
                }
        res = self.session.get(url='https://login.sina.com.cn/sso/prelogin.php', params=params)
        data = json.loads(re.findall(r'\((.*?)\)', res.text)[0])
        # print(data['pubkey'])
        return data

    # 2.提交登录请求
    def get_username(self):
        res = parse.quote(self.username)
        res = base64.b64encode(res.encode())
        return res.decode('utf-8')


    def get_password(self, pubkey, password):
        # publickey = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        # res = rsa.encrypt(password.encode(), publickey)
        # 生成公钥
        recipient_key = RSA.RsaKey(n=int(pubkey, 16), e=65537)
        # 创建rsa对象
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        # 加密数据+转换成16进制
        msg = binascii.b2a_hex(cipher_rsa.encrypt(password.encode())).decode()
        # print(msg)
        return msg   

    def make_check(self):
        #得到验证码
        check = {'pcid':'','door':''}
        check_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1561615767197'.format(self.get_username())
        res = self.session.get(check_url)
        res = json.loads(re.findall(r'preloginCallBack\((.*?)\)', res.text)[0])
        if res['showpin'] == 0:
            print('没有验证码')
            # self.login()
            return check
        else:
            print('有验证码')
            get_checkurl = 'https://login.sina.com.cn/cgi/pin.php?r=3877496&s=0&p={}'.format(res['pcid'])
            html = self.session.get(get_checkurl)
            now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
            fname= r"C:/Users/Administrator/Desktop/16期爬虫高级/05_js调试(五)/check/"+now+r"check.jpg"
            with open(fname, 'wb') as f:
                f.write(html.content)
            print("存储成功！")
            check['pcid'] = res['pcid']
            check['door'] = input("请输入验证码>>>")
            return check

    def login(self):
        data = self.get_pubkey()
        check = self.make_check()
        password = str(data['servertime']) + '\t' + data['nonce']+'\n'+ self.password
        form_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': '',
            'pcid': check['pcid'],
            'door': check['door'],
            'vsnf': 1,
            'su': self.get_username(),
            'service': 'miniblog',
            'servertime': data['servertime'],
            'nonce': data['nonce'],
            'pwencode': 'rsa2',
            'rsakv': data['rsakv'],
            'sp': self.get_password(data['pubkey'], password),
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': '49',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        #发起登入请求
        login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        res = self.session.post(url=login_url, data=form_data)
        res.encoding = 'gbk'
        print('登入请求发起成功：%s....' % (res.text[:20]))

        #提取重定向url
        next_url = re.findall(r'replace\("(.*?)"\)', res.text)[0]
        next_url = parse.unquote(next_url, encoding='gbk')
        print('提取重定向url成功：%s....' % (next_url[:20]))

        #发起重定向url请求
        response = self.session.get(next_url)
        response.encoding = 'gbk'
        print('重定向url请求成功：%s....' % (response.text[:20]))

        #提取登入必须url：
        urls = re.findall(r'arrURL":(.*?)}', response.text)[0]
        urls = json.loads(urls)
        print('提取登入必须url成功：%s....' % (urls))

        # url筛选提取
        res = self.session.get(urls[0])
        res.encoding = 'gbk'
        print('url筛选提取成功：%s....' % (res.text[:20]))

        #最后一步登入
        res = self.session.get('https://weibo.com/?wvr=5&lf=reg')
        print('登入成功：%s....' % (res.url[:20]))
        print(res.text)
        # return res.text

if __name__ == '__main__':
    username = '1092972423@qq.com'
    password = 'xl1229'
    user = '19914746604'
    pwd = '520.xm'
    # WeiboLogin(user, pwd).login()
    WeiboLogin(username, password).login()