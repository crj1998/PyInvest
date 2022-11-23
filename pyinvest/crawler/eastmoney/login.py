
import os
import math
import time
import json
import random
import pickle
import requests
import lxml.etree

from PIL import Image
from io import BytesIO
from base64 import b64encode
from tempfile import NamedTemporaryFile

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def encrypt(n):
    if n is None or n == '': return n

    def truncated(x):
        t = (0xffffffff & x) if x>=0 else -(0xffffffff & -x)
        if t > 2147483647: t = t - 4294967296
        return t


    def unsigned_right_shift(a, b):
        if a < 0:
            return (4294967296 + a) >> b
        else:
            return a>>b

    def left_shift(a, b):
        t = a<<b
        return truncated(t)

    def bitwise_xor(a, b):
        t = a^b
        return truncated(t)

    def bitwise_and(a, b):
        t = a&b
        return truncated(t)

    def i(x):
        t = (0xffffffff & x) if x>=0 else -(0xffffffff & -x)
        return truncated(t)

    # only ascii
    def r(n):
        return n

    def o(n, e, t, r, i, o):
        res = bitwise_xor(
            bitwise_xor(unsigned_right_shift(t, 5), left_shift(e, 2)) + bitwise_xor(unsigned_right_shift(e, 3), left_shift(t, 4)), 
            bitwise_xor(n, e) + bitwise_xor(o[bitwise_xor(bitwise_and(3, r), i)], t)
        )

        return res

    def a(n, e):
        r = len(n)
        i = r >> 2
        if i & 3 != 0: i += 1
        t = [0] * i
        if e: t.append(r)
        for o in range(r):
            t[o >> 2] |= ord(n[o]) << ((3 & o) << 3)
        return t

    t = "e98ae8878c264a7e"
    n = r(n)
    t = r(t)
    def anonymous1(n, e):
        d = len(n)
        u = d - 1
        r = n[u]
        a = 0
        l = 0 | math.floor(52/d)+6
        for l in range(l, 0, -1):
            a = i(a + 2654435769)
            s = bitwise_and(unsigned_right_shift(a, 2), 3)
            for c in range(u):
                t = n[c + 1]
                r = n[c] = i(n[c] + o(a, t, r, c, s, e))
            t = n[0]
            r = n[u] = i(n[u] + o(a, t, r, u, s, e))
        return n

    n = a(n, True)
    e = a(t, False)
    while len(e) < 4: e.append(0)

    n = anonymous1(n, e)

    def anonymous2(n, e):
        t = len(n)
        r = t << 2
        if e:
            i = n[t-1]
            r -= 4
            if i < r - 3 or i > r: return None
            r = i
        a = []
        for o in range(t):
            a.extend([
                n[o] & 0xff, unsigned_right_shift(n[o], 8) & 0xff, 
                unsigned_right_shift(n[o], 16) & 0xff, unsigned_right_shift(n[o], 24) & 0xff
            ])
        return a[:r] if e else a
    n = anonymous2(n, False)
    return b64encode(bytes(n)).decode()


def upload(filepath):
    ts = str(int(time.time()*1000))
    data = {
        'type': 'file',
        'action': 'upload',
        'timestamp': ts,
        'auth_token': '9d2219cce7bba9b3a18db9d91bd042719fddaf19',
        'expiration': 'PT30M'
    }
    files = {
        "source": (filepath, open(filepath, "rb"), "images/jpeg")
    }
    headers = {
        'origin': 'https://imgbb.com',
        'referer': 'https://imgbb.com/upload',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'
    }
    r = requests.post(url='https://imgbb.com/json', files=files, data=data, headers=headers)
    return r.json()['image']['url']

def decodeimg(url):
    w, h = 10, 80
    e = "6_11_7_10_4_12_3_1_0_5_2_9_8".split("_")
    offsets = []
    for r in range(52):
        n = 2 * int(e[r % 26 // 2]) + r % 2
        if (r//2) % 2 == 0: n += -1 if r%2 else 1
        n += 26 if r < 26 else 0
        offsets.append((n % 26 * 12 + 1, 80 if n<26 else 0))

    r = requests.get(url, timeout=5)
    img = Image.open(BytesIO(r.content))
    panel = Image.new('RGB', (img.size[0]//12*w, img.size[1]))
    for i, (x, y) in enumerate(offsets):
        nx, ny = i % 26 * w, i //26 * h
        panel.paste(img.crop((x, y, x+w, y+h)), (nx, ny, nx+w, ny+h))

    # Create a byte stream pipeline
    img_bytes = BytesIO()
    # Store the image data into the byte stream pipeline
    panel.save(img_bytes, format="JPEG")
    # Get the binary from the byte stream pipe
    image_bytes = img_bytes.getvalue()

    with NamedTemporaryFile(
        mode="w+b", delete=True, suffix='.jpg', prefix='pyinvest_'
    ) as f:
        f.write(image_bytes)
        filename = f.name
        url = upload(filename)
    # os.remove(filename)
    
    return url


class CookiesManagement(object):
    def __init__(self, filename=f"Cookies.dat"):
        self.Cookies = {}
        self.__filename = filename

    def load_cookies(self):
        if not(os.path.exists(self.__filename) and os.path.isfile(self.__filename)):
            with open(self.__filename, "wb") as f:
                pickle.dump(self.Cookies, f)
            return {}

        with open(self.__filename, "rb") as f:
            cookie = pickle.load(f)
        return cookie

    def save_cookies(self, cookie):
        if isinstance(cookie, dict):
            self.Cookies = cookie
            with open(self.__filename, "wb") as f:
                pickle.dump(self.Cookies, f)
            return True
        else:
            return False

class SimulateLogin(object):
    def __init__(self, username, password):
        self.__session = requests.Session()
        self.__cookies = CookiesManagement(f"Cookies.dat")
        self.__session.verify = False
        self.__user = username
        self.__pwd = password
        self.__rurl = ""
        self.__ctxid = ""
        self.__RequestVerificationToken = ""
        self.__validate = ""
        self.info = None
    
    def __repr__(self):
        return f'Account({self.info[0]})' if self.info else 'Account(unlogin)'

    def init_session(self):
        self.__session.headers.clear()
        self.__session.cookies.clear()
        self.__session.headers.update({
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        })
        self.__session.cookies.update({
            # "st_pvi": "79553158735204",
            # "st_sp": "2018-10-31%2016%3A58%3A51",
            # "em_hq_fls": "js",
            # "emhq_stock": "%2C600165",
            # "em-quote-version": "topspeed",
            # "emshistory": "%5B%22002451%22%2C%22000070%22%2C%22%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%22%2C%22jd%22%5D",
            # "Hm_lvt_557fb74c38569c2da66471446bbaea3f": "1542890740",
            # "HAList": "a-sz-164815-%u539F%u6CB9LOF%2Ca-sh-600090-%u540C%u6D4E%u5802%2Ca-sh-600086-%u4E1C%u65B9%u91D1%u94B0%2Ca-sz-150002-%u5927%u6210%u4F18%u9009%2Ca-sz-150026-%u666F%u4E30B%2Cl-sh-201000-R003%2Ca-sz-002451-%u6469%u6069%u7535%u6C14%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600021-%u4E0A%u6D77%u7535%u529B%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570",
            # "_qddaz": "QD.jtaya0.i20qb9.joso8tml",
            # "pgv_pvi": "5682077696",
            # "qgqp_b_id": "e95e4d8cc6967afef247d282a13e606b",
            # "st_si": "40545530256549",
            # "p_origin": "https%3A%2F%2Fpassport2.eastmoney.com"
        })

    # check valid of local cookies
    def cookies_test(self):
        localCookies = self.__cookies.load_cookies()
        if localCookies:
            self.__session.headers.update({
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9"
            })
            self.__session.cookies.update(localCookies)
            url = "https://passport2.eastmoney.com/pub/basicinfo"
            r = self.__session.get(url)
            html = lxml.etree.HTML(r.text)
            RequestVerificationToken = html.xpath("//input[@name='__RequestVerificationToken']")[0].get("value")
            self.__session.headers.update({
                "Referer": "https://passport2.eastmoney.com/pub/basicinfo",
                "Origin":"https://passport2.eastmoney.com",
                "Host": "passport2.eastmoney.com"
            })
            url = "https://passport2.eastmoney.com/pub/JsonAPI/GetUserInfo"
            r = self.__session.post(url, data={"__RequestVerificationToken":RequestVerificationToken})
            retdata = r.json()
            if retdata["rc"]:
                self.info = (retdata["result"]["Alias"],retdata["result"]["UID"])
                self.__session.headers.clear()
                return self.info
            else:
                self.init_session()
                return False
        else:
            self.init_session()
            return False

    def _pre_login(self):
        url = "https://passport2.eastmoney.com/pub/login"
        self.__session.headers.update({
            "Host": "passport2.eastmoney.com",
            "Referer": "http://www.eastmoney.com/"
        })
        params = {
            "backurl": "http://www.eastmoney.com/"
        }
        r = self.__session.get(url, params=params, timeout=5)

        url = "https://exaccount2.eastmoney.com/Home/Login"
        self.__session.headers.update({
            "Host": "exaccount2.eastmoney.com",
        })
        params = {
            "request": '{"agentPageUrl":"https://passport2.eastmoney.com/pub/LoginAgent","redirectUrl":"https://quote.eastmoney.com/sh516100.html","callBack":"LoginCallBack","redirectFunc":"PageRedirect","data":{"domainName":"passport2.eastmoney.com","deviceType":"Web","productType":"UserPassport","version":"0.0.1"}}'
        }
        r = self.__session.get(url, params=params, timeout=5)
        assert r.status_code==200, f'status code: {r.status_code}'
        self.__rurl = r.url
        html = lxml.etree.HTML(r.text)
        self.__ctxid = html.xpath("//input[@id='hdAccountCaptContextId']")[0].get("value")
        self.__RequestVerificationToken = html.xpath("//input[@name='__RequestVerificationToken']")[0].get("value")

    def _captcha_get(self):
        self.__session.headers.update({
            "Host": "smartvcode2.eastmoney.com",
            "Referer": self.__rurl
        })
        plaintext = {
            'appid': '201802274651',
            'ctxid': self.__ctxid,
            'a': self.__user,
            'p': self.__pwd,
            'r': str(random.random())[:19]
        }
        plaintext = '|'.join(f'{k}={v}' for k, v in plaintext.items())
        params = {
            # "callback": "cb",
            "ctxid": self.__ctxid,
            "request": encrypt(plaintext),
            "_": str(int(time.time()*1000))
        }
        url = "https://smartvcode2.eastmoney.com/Titan/api/captcha/get"
        r = self.__session.get(url, params=params, timeout=5)
        assert r.status_code==200, f'status code: {r.status_code}'
        r.encoding = r.apparent_encoding
        r = r.json()
        assert r['ReturnCode'] == '0', r['Msg']
        assert r['Data']['CaptchaType'] in ['init', 'word', 'click'], r['Data']['CaptchaType']
        r = json.loads(r['Data']['CaptchaInfo'])
        return r

    def _captcha_valid(self, ctype, u = None):
        url = "https://smartvcode2.eastmoney.com/Titan/api/captcha/Validate"
        if ctype == 'init':
            d = '7,35,0:7,33,205:7,25,227:66,38,5943:70,13,5967:71,6,5986:91,4,6371:92,10,6393:94,17,6414:95,22,6438:96,25,6460'
            u = ''
        elif ctype == 'word':
            assert u is not None
            u = str(u)
            d = '0,0,0:156,74,1026:149,63,1049:135,45,1072:133,43,1095:129,40,1117:123,36,1139:121,34,1162:115,29,1184:110,27,1207:108,26,1229:107,26,1320:105,26,1432:104,26,1462:102,25,1567:81,23,1590:55,21,1612:13,20,1634:0,20,1656:1,20,1777:3,20,1792:9,23,1815:17,24,1845:32,27,1882:38,27,1926:40,27,1957:41,27,1979:41,27,2016'
        elif ctype == 'click':
            assert u is not None
            u = u.split(" ")
            # x,y,t:x,y,t
            u = ':'.join(f'{u[2*i]},{u[2*i+1]},{0 if i==0 else random.randint(500*i, 500*i+400)}' for i in range(len(u)//2))
        
        plaintext = {
            'appid': '201802274651',
            'ctxid': self.__ctxid,
            'type': ctype,
            'u': u,
            # 'd': d,
            't': str(random.randint(500, 1500)),
            'a': self.__user,
            'p': self.__pwd,
            'r': str(random.random())[:19]
        }
        plaintext = '|'.join(f'{k}={v}' for k, v in plaintext.items())
        params = {
            # "callback": "cb",
            "ctxid": self.__ctxid,
            "request": encrypt(plaintext),
            "_": str(int(time.time()*1000))
        }
        r = self.__session.get(url, params=params)
        r.encoding=r.apparent_encoding
        r = r.json()
        return r

    def _captcha_check(self):
        r = self._captcha_get()
        r = self._captcha_valid(r['type'])
        r = self._captcha_get()
        src = ('https://' if r['https'] else 'http://') + r['static_servers'][0] + r['fullbg']
        url = decodeimg(src)
        if r['type'] == 'word':
            code = input(f'Click the {url} and input the {r["info"]} code: ')
        elif r['type'] == 'click':
            code = input(f'Click the {url} and input the location of {r["info"]}(x y): ')
        r = self._captcha_valid(r['type'], code)
        # self.__validate = str(r.text.split(",")[-2].split(":")[-1])[2:-2]
        self.__validate = json.loads(r['Data']['Result'])['validate']

    def _post_login(self):
        url = "https://exaccount2.eastmoney.com/JsonAPI/Login3"
        self.__session.headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Host": "exaccount2.eastmoney.com",
            "domainName": "passport.eastmoney.com",
            "Origin": "https://exaccount2.eastmoney.com",
            "Referer": self.__rurl,
            "X-Requested-With": "XMLHttpRequest",
            "deviceType": "Web",
            "productType": "UserPassport",
            "version": "0.0.1",
            "RequestVerificationToken": self.__RequestVerificationToken
        })
        data = {
            "username": self.__user,
            "password": self.__pwd,
            "captconetxt": self.__ctxid,
            "captvalidate": self.__validate
        }
        r = self.__session.post(url, data=data, timeout=5)
        retdata = r.json()
        if retdata["rc"]:
            self.info = (retdata["result"]["Alias"], retdata["result"]["UID"])
            ret = requests.utils.dict_from_cookiejar(r.cookies)
            self.__cookies.save_cookies(ret)
            self.__session.headers.clear()
            return self.info
        else:
            print(f'[{retdata["errorcode"]}]{retdata["error"]}')
            return False

    def _send_active_code(self):
        url = 'https://exaccount2.eastmoney.com/JsonAPI/SendActiveCodeForLogin3'
        data = {
            'InterCode': '86',
            'PhoneNumber': '18217380385',
            "captconetxt": self.__ctxid,
            "captvalidate": self.__validate
        }
        r = self.__session.post(url, data=data, timeout=5)
        r = r.json()
        apicontext = r['result']['ApiContext']
        captcontext = r['result']['CaptContext']
        mobileactivecodecontext = r['result']['MobileActiveCodeContext']
        activecode = input('phone code: ')
        url = 'https://exaccount2.eastmoney.com/JsonAPI/MobileLoginByActiveCode'
        data = {
            'InterCode': '86',
            'PhoneNumber': '18217380385',
            'ActiveCode': activecode,
            "MobileActiveCodeContext": mobileactivecodecontext,
            "ApiContext": apicontext
        }
        r = self.__session.post(url, data=data, timeout=5)
        r = r.json()
        return 

    def login(self):
        if self.cookies_test():
            return self.__session

        self._pre_login()
        self._captcha_check()
        ret = self._post_login()
        return self.__session if ret else False

if __name__ == '__main__':
    account = SimulateLogin("18217480940", "testpwd")
    session = account.login()
    print(session)
    print(account)
    
    """
    first correct: direct
    second: word
    wrong: click
    """

