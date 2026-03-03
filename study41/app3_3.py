from bs4 import BeautifulSoup as bs
from requests import get
import json
from mariadb_crud import save, saveMany
from settings import settings

def getLikes(list, head=None):
  ids = ""
  for i in range(len(list)):
    if i == 0:
      ids += f"{list[i]["id"]}"
    else:
      ids += f",{list[i]["id"]}"
  if ids:
    url = f"https://www.melon.com/commonlike/getSongLike.json?contsIds={ids}"
    res = get(url, headers=head)
    if res.status_code == 200:
      data = json.loads(res.text)
      for row in data["contsLike"]:
        for i in range(len(list)):
          if list[i]["id"] == row["CONTSID"]:
            list[i]["cnt"] = row["SUMMCNT"]
            break
  return list

def getData(data, gnrCode):
  arr = []
  trs = data.select("#frm tbody > tr")
  if trs:
    for i in range(len(trs)):
      id = int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value"))
      img = cleanData(trs[i].select("td")[2].select_one("img")["src"])
      title = cleanData(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text)
      album = cleanData(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text)
      arr.append( {"id": id, "img": img, "title": title, "album": album, "cnt": 0, "code": gnrCode} )
  return arr

def cleanData(txt):
  list = ["\n", "\xa0", "\r", "\t", "총건수"]
  for target in list:
    txt = txt.replace(target, "")
  return txt.strip()

def crawlingMelon(gnrCode: str, head=None):
  if head is None:
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
  url = f"https://www.melon.com/genre/song_list.htm?gnrCode={gnrCode}&orderBy=POP"
  res = get(url, headers=head)
  arr = []
  if res.status_code == 200:
    data = bs(res.text, 'lxml')
    arr = getData(data, gnrCode)
    arr = getLikes(arr, head)
    sql1 = f"""
            select 1
            """
    sql2 = f"""
          INSERT INTO edu.`melon` 
          (`id`, `img`, `title`, `album`, `cnt`, `code`)
          VALUE
          (%s, %s, %s, %s, %s, %s)
          ON DUPLICATE KEY UPDATE
            img=VALUES(img),
            title=VALUES(title),
            album=VALUES(album),
            cnt=VALUES(cnt),
            code=VALUES(code)
        """
    values = [(row["id"], row["img"], row["title"], row["album"], row["cnt"], row["code"]) for row in arr]
    saveMany(sql1, sql2, values)
  return arr

def save_all_genres(a,b):
    for i in range(a, (b+1)):
        gnrCode = f"GN0{i}00"
        print(f"{gnrCode} 수집 중...")
        crawlingMelon(gnrCode)

# crawlingMelon("GN0100")
# crawlingMelon("GN0200")
# crawlingMelon("GN0300")
save_all_genres(1,3)
