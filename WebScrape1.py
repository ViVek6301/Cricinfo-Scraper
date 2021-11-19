import requests
from bs4 import BeautifulSoup
import pandas as pd

# req = requests.get("https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=start;size=200;spanmin1=01+Jan+1975;spanval1=span;template=results;type=aggregate;view=match")
req = requests.get("https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;home_or_away=1;host=6;opposition=1;spanmin1=15+Mar+2001;spanval1=span;team=6;template=results;type=bowling;view=match")
soup = BeautifulSoup(req.content, "html.parser")
tables = soup.find_all('table', class_ = 'engineTable')

fields = [] # fields stores the various headers in the query

dataTable = tables[2]

tableHead = dataTable.thead.tr
headers = tableHead.findAll('th')

for header in headers:
    if header.text != '':
        fields.append(header.text)

print(fields)
n = fields.__len__()
lists = []
for i in range(n):
    lists.append([])

rows = dataTable.tbody.findAll('tr')

for row in rows:
    cols = row.findAll('td')
    j = 0
    for col in cols:
        if col.text != '':
            lists[j].append(col.text)
            j += 1

resultDict = {}
for i in range(len(fields)):
    resultDict[fields[i]] = lists[i]

df = pd.DataFrame(resultDict)
print(df.head())
