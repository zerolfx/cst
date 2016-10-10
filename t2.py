import re
import bs4

with open('t2.html', 'r') as f:
    r = f.read()
soup = bs4.BeautifulSoup(r, 'html.parser')

column = len(soup.rows.head.find_all('column'))-1
row = len(soup.rows.find_all('row'))
print(row)

# l = [[None] * column] * row
l = [[None for c in range(column)] for r in range(row)]
for row in soup.rows.find_all('row'):
    c = row.find_all('cell')
    for j in range(0, column):
        # print(c[j+1].string)
        l[int(row['id'])-1][j] = c[j+1].string
        if c[j+1].has_key('style') and 'gray' in c[j+1]['style']:
            l[int(row['id'])-1][j] = 'disabled'
print(l)