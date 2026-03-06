from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
import streamlit as st
import json

st.set_page_config(
  page_title="yes24 수집",
  page_icon="💗",
  layout="wide",
)

# Yes24 베스트셀러 URL 예시
# https://www.yes24.com/product/category/weekbestseller?categoryNumber=001&pageNumber=1&pageSize=40&type=week&saleYear=2026&weekNo=1149&sex=A&viewMode=thumb
yes24 = "https://www.yes24.com/product/category/weekbestseller"
categoryNumber = "001"
pageNumber = 1
pageSize = 40
type = "week"
saleYear = 2026
weekNo = 1149
sex = "A"
viewMode = "thumb"

url = (
  f"{yes24}?"
  f"categoryNumber={categoryNumber}&"
  f"pageNumber={pageNumber}&"
  f"pageSize={pageSize}&"
  f"type={type}&"
  f"saleYear={saleYear}&"
  f"weekNo={weekNo}&"
  f"sex={sex}&"
  f"viewMode={viewMode}"
)

# 데이터 수집
def getData():
  try:
    # url = ""
    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
    st.text(f"URL: {url}")
    res = get(url, headers=head)
    if res.status_code == 200:
      st.text("yes24 국내도서 주별 베스트 수집 시작!")
      soup = bs(res.text, 'lxml')
      table = soup.select_one("#yesBestList")
      rows = table.select(".itemUnit")
      books = [] # { 도서명, 저자, 별점 }
      for row in rows:
        title_row = row.select_one(".gd_name")
        if title_row:
          title = title_row.get_text(strip=True) if title_row else "제목 없음"
        author_row = row.select_one(".info_auth").find("a")
        if author_row:
          author = author_row.get_text(strip=True) if author_row else "저자 미상"
        rating_row = row.select_one(".rating_grade .yes_b")
        if rating_row:
          rating = rating_row.get_text(strip=True) if rating_row else "별점 없음"
        books.append({
          "title" : title,
          "author" : author,
          "rating" : rating
        })
      tab1, tab2, tab3 = st.tabs(["HTML 데이터", "JSON 데이터", "DataFrame"])
      with tab1:
        st.text("html 출력")
        st.html(rows)
      with tab2:
        st.text("JSON 출력")
        json_string = json.dumps(books, ensure_ascii=False, indent=2)
        st.json(body=json_string, expanded=True, width="stretch")
      with tab3:
        st.text("DataFrame 출력")
        st.dataframe(
          pd.DataFrame(books),
          width='stretch'
        )
  except Exception as e:
    return 0
  return 1

if st.button(f"수집하기"):
  getData()