import requests
import re
import html
Verify_Pre_URL = 'http://www.cst.ecnu.edu.cn/pages/148/'
Verify_URL = 'http://www.cst.ecnu.edu.cn/pages/152/'
Login_URL = 'http://www.cst.ecnu.edu.cn/pages/118/'
Error_RE = re.compile(r'eid=".*">(.*?)</STATUS></ROOT>')
Username_RE = re.compile(r'label="真实姓名".*?value="(.*?)"/>')


class Login:
    def __init__(self, username, password):
        self.s = requests.Session()
        self.usr = username
        self.pwd = password

    def get_verify(self):
        self.s.get(Verify_Pre_URL)
        r = self.s.get(Verify_URL)
        # print(r.content)
        with open('t.png', 'wb') as img:
            img.write(r.content)

    def login(self, vcode):
        data = {'tagid': '100', 'loginname': self.usr, 'password': self.pwd, 'state': 'online', 'vcode_login': vcode}
        r = self.s.post(Login_URL, data=data).text
        if 'success' not in r:
            # TODO error
            print(html.unescape(re.search(Error_RE, r).group(1)))

    def get_cookies(self):
        return self.s.cookies.get_dict()


def get_username(cookies):
    s = requests.Session()
    s.cookies.update(cookies)
    s.get('http://www.cst.ecnu.edu.cn/pages/151/')
    r = html.unescape(s.get('http://www.cst.ecnu.edu.cn/pages/154/').text)
    if '真实姓名' in r:
        return re.search(Username_RE, r).group(1)

if __name__ == '__main__':
    z = Login('10165102122', 'password')
    z.get_verify()
    z.login(input('verify code?\n'))
    print(z.get_cookies())
    print(get_username(z.get_cookies()))
