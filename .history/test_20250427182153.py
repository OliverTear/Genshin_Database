from urllib.request import Request, urlopen, urlretrieve, install_opener, build_opener
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
        # URLの指定

url = "https://wikiwiki.jp/genshinwiki/%E6%AD%A6%E5%99%A8/%E4%B8%80%E8%A6%A7"
headers = {
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
}
request = Request(url, headers=headers)
html = urlopen(request).read()
bsObj = BeautifulSoup(html, 'html.parser')
# テーブルを指定
table = bsObj.findAll("table")[1]
for table in bsObj.findAll("table"):
    for tab in table:
        rows = tab.find_all("tr")
        Allrows = []
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            Allrows.append(csvRow)
    sqlitelist = []
    print(Allrows)
    for row in Allrows:
        if row[0] == "☆5":
            row[0] = "5"
        elif row[0] == "☆4":
            row[0] = "4"
        elif row[0] == "☆3":
            row[0] = "3"
        elif row[0] == "☆2":
            row[0] = "2"
        elif row[0] == "☆1":
            row[0] = "1"
        if row[15] == "―":
            row[15] = "0"
        row[10] = row[10].replace(",", "")
        sqlitelist.append(f'INSERT INTO WeaponList(type, rarity, name, BASEATK, SubEffect, CollectionValue, ElementalEnergy, Version) VALUES("{row[1]}", "{row[2]}", {row[3]}, "{row[4]}", "{row[5]}", "{row[6]}", "{row[7]}", "{row[8]}", "{row[9]}", {row[10]}, {row[11]}, {row[12]}, "{row[13]}", "{row[14]}", {row[15]}, {row[16]})')