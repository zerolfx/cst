import bs4
import time
import re
with open('t.html', 'r') as f:
    t = f.read()
# print(t)

s = bs4.BeautifulSoup(t, 'html.parser')
'''
rows = s.find_all('row')
row = rows[2]
print(row['style'])
print('+++++++++++++++++=')
cells = row.find_all('cell')
for cell in cells:
    print(cell.string)
'''
today = time.strftime("%Y-%m-%d")
now = time.time()
l = []
for row in s.find_all('row'):
    if 'blue' in row['style']:
        cells = row.find_all('cell')
        if cells[3].string == today:
            print([x.string for x in cells])
            start_time = time.mktime(time.strptime(today+' '+cells[4].string[:5], '%Y-%m-%d %H:%S'))
            end_time = time.mktime(time.strptime(today+' '+cells[4].string[-5:], '%Y-%m-%d %H:%S'))
            # print(start_time, end_time, time.time())
            # if start_time <= now <= end_time:
            # print(cells[1].string)
            name = re.search(r'^(.*?)\^', cells[1].string).group(1)
            aid = cells[0].string
            l.append(dict(name=name, aid=aid))
#  18:30 - 21:30
# 2016-10-08
print(time.strptime('18:30', '%H:%S'))