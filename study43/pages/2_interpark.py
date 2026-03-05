from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
import streamlit as st
import json

st.set_page_config(
  page_title="interpark 수집",
  page_icon="💗",
  layout="wide",
)

# 인터파크 장르별 URL
# 뮤지컬 url
musical_url = "https://tickets.interpark.com/contents/ranking?genre=MUSICAL"
# 콘서트 url
concert_url = "https://tickets.interpark.com/contents/ranking?genre=CONCERT"
# 클래식 url
classic_url = "https://tickets.interpark.com/contents/ranking?genre=CLASSIC"
# 아동 url
kids_url = "https://tickets.interpark.com/contents/ranking?genre=KIDS"
# 연극 url
drama_url = "https://tickets.interpark.com/contents/ranking?genre=DRAMA"
# 전시 url
exhibit_url = "https://tickets.interpark.com/contents/ranking?genre=EXHIBIT"

# 데이터 수집
def getData():
  try:
    url = musical_url
    st.text(f"URL: {url}")
    genre = url.split("genre=")[-1] if "genre=" in url else "알 수 없음"
    tickets = [] # { 장르, 티켓이름, 장소, 시작날짜, 종료날짜, 예매율 }
    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
    res = get(url, headers=head)
    if res.status_code == 200:
      st.text("인터파크 티켓 수집 시작!")
      soup = bs(res.text, 'lxml')
      rows = soup.select(".responsive-ranking-list_rankingItem__PuQPJ")
      for row in rows:
        title_row = row.select_one(".responsive-ranking-list_goodsName__aHHGY")
        if title_row:
          title = title_row.get_text(strip=True) if title_row else "제목 없음"
        tickets.append({
          "genre": genre,
          "title" : title

          })
    tab1, tab2, tab3 = st.tabs(["HTML 데이터", "JSON 데이터", "DataFrame"])
    with tab1:
      st.text("html 출력")
      st.text(rows)
    with tab2:
      json_string = json.dumps(tickets, ensure_ascii=False, indent=2)
      st.text("JSON 출력")
      st.json(body=json_string, expanded=True, width="stretch")
    with tab3:
      st.text("DataFrame 출력")
  except Exception as e:
    return 0
  return 1

if st.button(f"수집하기"):
  getData()
