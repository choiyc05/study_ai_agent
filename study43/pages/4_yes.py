from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
import streamlit as st
import json

st.set_page_config(
  page_title="yes24 주간 베스트셀러 수집",
  page_icon="📖",
  layout="wide",
)

if 'link_index' not in st.session_state:
  st.session_state.link_index = 0

links = [
  "https://www.yes24.com/product/category/weekbestseller?pageNumber=1&pageSize=50&categoryNumber=001&type=week&saleYear=2026",
  "https://www.yes24.com/product/category/weekbestseller?pageNumber=1&pageSize=50&categoryNumber=002&type=week&saleYear=2026",
  "https://www.yes24.com/product/category/weekbestseller?pageNumber=1&pageSize=50&eBookTp=0&categoryNumber=017&type=week&saleYear=2026"
]

options = ["국내도서", "외국도서", "eBook"]

# Yes24 베스트셀러 URL 예시
# yes24 = "https://www.yes24.com/product/category/weekbestseller"
# categoryNumber = "001"
# pageNumber = 1
# pageSize = 40
# type = "week"
# saleYear = 2026
# weekNo = 1149
# sex = "A"
# viewMode = "thumb"

# url = (
#   f"{yes24}?"
#   f"categoryNumber={categoryNumber}&"
#   f"pageNumber={pageNumber}&"
#   f"pageSize={pageSize}&"
#   f"type={type}&"
#   f"saleYear={saleYear}&"
#   f"weekNo={weekNo}&"
#   f"sex={sex}&"
#   f"viewMode={viewMode}"
# )

# 데이터 수집
def getData():
  try:
    st.text("데이터 수집을 시작 합니다.")
    url = links[st.session_state.link_index]
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = get(url, headers=head)

    if res.status_code == 200:
      books = []
      soup = bs(res.text)
      items = soup.select("#yesBestList > li")
      
      for item in items:
        # 도서명
        title = item.select_one('.gd_name').get_text(strip=True)
        
        # 저자
        author_span = item.select_one("span.authPub.info_auth")
        author = "저자미상"
        if author_span:
          author_a = author_span.select_one("a")
          author = author_a.get_text(strip=True) if author_a else author_span.get_text(strip=True)

          # if author_a:
          #   author = author.get_text(strip=True)
          # else:
          #   author = author_span.get_text(strip=True)

        # author = author_span.select_one("a").get_text(strip=True)

        # 평점
        star_span = item.select_one("span.rating_grade")
        star = "0.0"
        if star_span:
          star_em = star_span.select_one("em.yes_b")
          star = star_em.get_text(strip=True) if star_em else star_span.get_text(strip=True)
        # star = star_span.select_one("em.yes_b").get_text(strip=True)

        # 가격
        price_strong = item.select_one("strong.txt_num")
        price = "가격정보없음"
        if price_strong:
          price_em = price_strong.select_one("em.yes_b")
          price = price_em.get_text(strip=True) if price_em else price.get_text(strip=True)
        # price = price_strong.select_one("em.yes_b").get_text(strip=True)

        books.append({"도서명" : title, "저자" : author, "평점" : star, "가격" : f"{price}원"})

      tab1, tab2, tab3 = st.tabs(["HTML 데이터", "JSON 데이터", "DataFrame"])
      with tab1:
        # st.text("HTML 데이터")
        st.html(items)
      with tab2:
        # st.text("JSON 데이터")
        json_string = json.dumps(books, ensure_ascii=False, indent=2)
        st.json(body=json_string, expanded=True, width="stretch")
      with tab3:
        st.text("DataFrame")
        st.dataframe(pd.DataFrame(books))
  except Exception as e:
    return 0
  return 1

st.title("yes24 주간 베스트셀러")

selected = st.selectbox(
  label="yes24 베스트셀러",
  options=options,
  index=None,
  placeholder="수집 대상을 선택하세요"
)

if selected:
  st.session_state.link_index = options.index(selected)
  if st.button(f"주간 베스트셀러 '{options[st.session_state.link_index]}' 수집"):
    if getData() == 0:
      st.text("수집된 데이터가 없습니다.")
