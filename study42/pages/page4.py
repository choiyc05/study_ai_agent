import streamlit as st
import time
from bs4 import BeautifulSoup as bs
from requests import get
import json
import pandas as pd

episode_links = [
	"https://en.wikipedia.org/wiki/Demon_Slayer:_Kimetsu_no_Yaiba_season_1",
	"https://en.wikipedia.org/wiki/Demon_Slayer:_Kimetsu_no_Yaiba_season_2",
	"https://en.wikipedia.org/wiki/Demon_Slayer:_Kimetsu_no_Yaiba_season_3",
	"https://en.wikipedia.org/wiki/Demon_Slayer:_Kimetsu_no_Yaiba_season_4",
]
options = ["Season1","Season2","Season3","Season4"]

if 'link_index' not in st.session_state:
    st.session_state.episode_index = 0

st.set_page_config(
	page_title="3. 위키백과 수집",
	page_icon="💗",
	layout="wide",
)

def main():
    try:
        st.text("수집 시작")
        url = episode_links[st.session_state.episode_index]
        head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = get(url, headers=head)
        if res.status_code == 200:
            # st.html(res.text)
            episodes = []
            soup = bs(res.text, 'lxml')
            table = soup.select_one("table.wikitable.plainrowheaders.wikiepisodetable") # 직접 html elements보고 작성
            rows = table.select("tr.vevent.module-episode-list-row")
            for i, row in enumerate(rows, start=1):
                synopsis = None
                synopsis_row = row.find_next_sibling("tr", class_="expand-child")
                if synopsis_row:
                    synopsis_cell = synopsis_row.select_one("td.description div.shortSummaryText")
                    synopsis = synopsis_cell.get_text(strip=True) if synopsis_cell else None
                episodes.append({
                    "season":  options[st.session_state.episode_index],
                    "episode_in_season": i,
                    "synopsis": synopsis
                })
            tab1, tab2, tab3 = st.tabs(["HTML 데이터", "JSON 데이터", "DataFrame"])
            with tab1:
                st.html(table)
            with tab2:
                json_string = json.dumps(episodes, ensure_ascii=False, indent=2)
                st.download_button(
                    label="JSON 다운로드",
                    data=json_string,
                    file_name=f"귀멸의칼날_{options[st.session_state.episode_index]}.json",
                    mime="application/json"
                )
                st.json(body=json_string, expanded=True, width="stretch")
            with tab3:
                st.dataframe(
                    pd.DataFrame(episodes).drop(columns=['season']),
                    use_container_width=True
                )
        st.text("데이터 수집이 완료 되었습니다.")
    except Exception as e:
        return 0
    return 1


st.title("[3] 위키백과 수집")

selected = st.selectbox(
    label="귀멸의 칼날",
    options=options,
    index=None,
    placeholder="수집 대상을 선택하세요."
)

if selected:
    st.session_state.episode_index = options.index(selected)
    if st.button(f"귀멸의 칼날 '{options[st.session_state.episode_index]}' 수집"):
        if main() == 0:
            st.text("수집된 데이터가 없습니다.")
        