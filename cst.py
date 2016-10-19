import requests
import re
import html
import os
import time
import bs4
Verify_Pre_URL = 'http://www.cst.ecnu.edu.cn/pages/148/'
Verify_URL = 'http://www.cst.ecnu.edu.cn/pages/152/'
Login_URL = 'http://www.cst.ecnu.edu.cn/pages/118/'
Error_RE = re.compile(r'eid=".*">(.*?)</STATUS></ROOT>')
Username_RE = re.compile(r'label="真实姓名".*?value="(.*?)"/>')


def get_verify(filename):
    s = requests.Session()
    s.get(Verify_Pre_URL)
    r = s.get(Verify_URL)
    with open('/home/zerol/PycharmProjects/flask_project/static/img/'+filename+'.png', 'wb') as img:
        img.write(r.content)
    return s.cookies.get_dict()


def login(username, password, vcode, cookies):
    data = {'tagid': '100', 'loginname': username, 'password': password, 'state': 'online', 'vcode_login': vcode}
    r = requests.post(Login_URL, data=data, cookies=cookies).text
    if 'success' not in r:
        return html.unescape(re.search(Error_RE, r).group(1))


def get_username(cookies):
    s = requests.Session()
    s.cookies.update(cookies)
    s.get('http://www.cst.ecnu.edu.cn/pages/151/')
    r = html.unescape(s.get('http://www.cst.ecnu.edu.cn/pages/154/').text)
    if '真实姓名' in r:
        return re.search(Username_RE, r).group(1)


def delete_img(filename):
    path = '/home/zerol/PycharmProjects/flask_project/static/img/'+filename+'.png'
    if os.path.isfile(path):
        os.remove(path)


def filter_room(cookies):
    s = requests.Session()
    s.cookies.update(cookies)
    s.get('http://www.cst.ecnu.edu.cn/pages/1701/')
    r = s.get('http://www.cst.ecnu.edu.cn/pages/341/').text
    today = time.strftime("%Y-%m-%d")
    now = time.time()
    l = []
    for row in bs4.BeautifulSoup(r, 'html.parser').find_all('row'):
        if 'blue' in row['style']:
            cells = row.find_all('cell')
            if cells[3].string == today:
                print([x.string for x in cells])
                start_time = time.mktime(time.strptime(today + ' ' + cells[4].string[:5], '%Y-%m-%d %H:%S'))
                end_time = time.mktime(time.strptime(today + ' ' + cells[4].string[-5:], '%Y-%m-%d %H:%S'))
                if start_time <= now:
                    name = re.search(r'^(.*?)\^', cells[1].string).group(1)
                    aid = cells[0].string
                    if now <= end_time:
                        l.append(dict(name=name, aid=aid, status=1))
                    else:
                        l.append(dict(name=name, aid=aid, status=0))
    return l


def get_room_length(cookies, aid):
    s = requests.Session()
    s.cookies.update(cookies)
    s.get('http://www.cst.ecnu.edu.cn/pages/1862/?aid='+aid)
    r = s.get('http://www.cst.ecnu.edu.cn/pages/1868/?aid='+aid).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    column = len(soup.rows.head.find_all('column')) - 1
    row = len(soup.rows.find_all('row'))
    return row, column


def get_room(cookies, aid):
    s = requests.Session()
    s.cookies.update(cookies)
    s.get('http://www.cst.ecnu.edu.cn/pages/1862/?aid='+aid)
    r = s.get('http://www.cst.ecnu.edu.cn/pages/1868/?aid='+aid).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    column = len(soup.rows.head.find_all('column')) - 1
    row = len(soup.rows.find_all('row'))
    l = [[None for c in range(column)] for r in range(row)]
    for row in soup.rows.find_all('row'):
        c = row.find_all('cell')
        for j in range(0, column):
            l[int(row['id']) - 1][j] = c[j + 1].string
            if c[j + 1].has_attr('style') and 'gray' in c[j + 1]['style']:
                l[int(row['id']) - 1][j] = 'disabled'
    return l, row, column

if __name__ == '__main__':
    cookies = get_verify('t')
    login('10165102122', 'password', input('vcode?\n'), cookies)
    print(filter_room(cookies))
    print(get_room(cookies, '1'))
