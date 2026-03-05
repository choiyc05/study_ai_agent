import streamlit as st
from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
import json

st.set_page_config(
    page_title="일간('daily') 랭킹 수집",
    page_icon="💗",
    layout="wide",
)

# url
# mapi.ticketlink.co.kr : 티켓링크의 모바일 API 서버 도메인
# /mapi/ranking/genre/daily : 장르별 일간 랭킹 API
# categoryId=10 : 상위 카테고리 (예: 공연)
# categoryId2=16 : 세부 장르 (예: 뮤지컬)
# categoryId3=0 : 추가 하위 분류 (없음을 의미)
# menu=RANKING : 랭킹 메뉴 지정
url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=16&categoryId3=0&menu=RANKING"


def getData():
    try:
        # url = ""
        st.text(f"URL: {url}")
        res = get(url)
        if res.status_code == 200:
            st.text("API 데이터 수집 시작!")
            json_data = json.loads(res.text)
            tab1, tab2, tab3 = st.tabs(["api 데이터", "JSON 데이터", "DataFrame"])
            with tab1:
                st.text("api 기본 출력")
                st.json(res.text,expanded=True, width="stretch")
            with tab2:
                st.text("JSON 출력")
                st.json(json_data.get("data", {}), expanded=False, width="stretch")
                st.html("<hr/>")
                st.text("랭킹 목록 출력")
                st.json(json_data.get("data", {}).get("rankingList", []), expanded=False, width="stretch")
            with tab3:
                st.text("DataFrame 출력")
                st.dataframe(pd.DataFrame(json_data.get("data", {}).get("rankingList", [])))
    except Exception as e:
        return 0
    return 1


st.title("3. 티켓링크 daily 랭킹 수집 (api)")
if st.button(f"수집하기"):
    getData()
