import requests
import re
import html
import sys
import os
import time
import bs4
Verify_Pre_URL = 'http://www.cst.ecnu.edu.cn/pages/148/'
Verify_URL = 'http://www.cst.ecnu.edu.cn/pages/152/'
Login_URL = 'http://www.cst.ecnu.edu.cn/pages/118/'
Error_RE = re.compile(r'eid=".*">(.*?)</STATUS></ROOT>')
Username_RE = re.compile(r'label="真实姓名".*?value="(.*?)"/>')
IMG_PATH = sys.path[0]+'/static/img/'


def get_verify(filename):
    s = requests.Session()
    s.get(Verify_Pre_URL)
    r = s.get(Verify_URL)
    with open(IMG_PATH+filename+'.png', 'wb') as img:
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
    path = IMG_PATH+filename+'.png'
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
                if now <= end_time:
                    name = re.search(r'^(.*?)\^', cells[1].string).group(1)
                    aid = cells[0].string
                    if now >= start_time:
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
    '''
    cookies = get_verify('t')
    login('10165102122', 'password', input('vcode?\n'), cookies)
    print(filter_room(cookies))
# [{'aid': '64', 'name': '晚自习519/525[续晋华]', 'status': 0}, {'aid': '68', 'name': '晚自习527/533[续晋华]', 'status': 0}, {'aid': '60', 'name': '晚自习B511/517[金健]', 'status': 0}]
    print(get_room(cookies, '1'))
# ([[' ', '乔丹', '陶玮', '付志超', '赵昊颖', '李孟航', '邬淑彦', 'disabled', 'disabled', 'disabled'], [' ', '钟鸣', '焦乙竹', '孙校珩', '王宁霞', '刁小桐', '王江舟', '苏晓慧', '武耐池', '莫光雪'], [' ', '林耀松', '任梦薇', '张舒燕', '周于瑞', '王诺', '路梦珂', '庞瑞', '贾博舒', '武蔡丽'], [' ', '郭德闻', '曹董', '郭玲燕', '陈晓萍', '汪尉蓝', '桑青园', '张巧梅', '徐翊宸', '李豪杰'], ['林兰', '顾睿珺', '杨诗文', '杨天强', '郭锦帅', ' ', '朱泽阳', '陈琳琳', '许媛媛', '李春阳'], [' ', '韦阳', '高思远', '崔阳光', '何梦雨', '余光宇', '吴凯', '胡子威', ' ', ' '], [' ', '徐佳炜', '施越', '侯之恒', '吕慧妍', '陆豪', '王辰奕', '黄弘毅', '王玥娇', ' '], ['黄子寅', '苏浩然', '樊洪森', '姚岳坤', ' ', ' ', '赵康哲', '郑淇', ' ', ' '], [' ', '曹卓群', ' ', '吴琪', '唐慧', '季茜', '陈圆', '邱正昊', '叶铭', ' '], [' ', '李轲', '殷正航', '余苏', ' ', '李天', '王馨苑', '岳孚嘉', '吴亿', ' '], ['方超', '普竹语', '李昶臻', '匡筱璐', '郭双怡', '宋雪', '张莉玲', 'disabled', 'disabled', 'disabled'], ['黄平', '吴俊涛', '周顺凯', '袁小杰', '李培勇', '毛鑫', '吴一钺', 'disabled', 'disabled', 'disabled'], [' ', '林泊润', '彭贝城', '周晔', '赖俊宇', '齐强', '费鼎淳', '郝杉', ' ', '黄园苑|李智伟']], <row id="13"><cell><![CDATA[13]]></cell><cell style="background-color:DarkSeaGreen"><![CDATA[ ]]></cell><cell><![CDATA[林泊润]]></cell><cell><![CDATA[彭贝城]]></cell><cell><![CDATA[周晔]]></cell><cell><![CDATA[赖俊宇]]></cell><cell><![CDATA[齐强]]></cell><cell><![CDATA[费鼎淳]]></cell><cell><![CDATA[郝杉]]></cell><cell style="background-color:DarkSeaGreen"><![CDATA[ ]]></cell><cell style="background-color:LightPink"><![CDATA[黄园苑|李智伟]]></cell></row>, 10)
    '''