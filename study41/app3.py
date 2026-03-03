from bs4 import BeautifulSoup as bs
from requests import get
import json

url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100"
url2 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=601405898%2C601408401%2C601412950%2C601412107%2C601430732%2C601416574%2C601416570%2C601416535%2C601416271%2C601416261%2C601416212%2C601415215%2C601414111%2C601413850%2C601413800%2C601413798%2C601413742%2C601413738%2C601413550%2C601413408%2C601413390%2C601413333%2C601413080%2C601412960%2C601405270%2C601407441%2C601413060%2C601393896%2C601407916%2C601412828%2C601405642%2C601407906%2C601413104%2C601413051%2C601416316%2C601416284%2C601416282%2C601416281%2C601415505%2C601415360%2C601415299%2C601414109%2C601414105%2C601413819%2C601413249%2C601413233%2C601413216%2C601407817%2C601407812%2C601405239"

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}

res = get(url, headers=head)
res2 = get(url2, headers=head)

ids = []
images = []
titles = []
albums = []
likes = []
cnts = []

if res2.status_code == 200:
    jData = json.loads(res2.text)
    for row in jData["contsLike"]:
        cnts.append({"CONTSID": row["CONTSID"], "SUMMCNT": row["SUMMCNT"]})

if res.status_code == 200:
    data = bs(res.text, 'lxml')
    # print(data)
    title = data.title.text
    trs = data.select("#frm tbody > tr")
    
    for i in range(len(trs)):
        images.append(trs[i].select("td")[2].select_one("img").get("src"))
        titles.append(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text.replace("\n", "").replace("\xa0", " ").strip()) # strip() : 여백 지우기 (양쪽 끝)
        albums.append(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text.replace("\xa0", " ").strip())
        ids.append(int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value")))

    for id in ids:
        for row in cnts:
            # if id == 601408401:
            #     print(id, row["CONTSID"], id == row["CONTSID"])
            if id == row["CONTSID"]:
                likes.append(row["SUMMCNT"])
                # print(row["SUMMCNT"])


print(f"곡 제목 : {titles}")
print(f"앨범 이미지 : {images}")
print(f"앨범 : {albums}")
print(f"좋아요 : {likes}")

