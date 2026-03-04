import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title="2. 암환자수 통계",
	page_icon="💗",
	layout="wide",
)

if 'slider_value' not in st.session_state:
    st.session_state.slider_value = (2017,2022)

url = "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=277002&idx_cd=2770&freq=Y&period=N"

st.title("[2] 암환자수 통계")
col1, col2, col3 = st.tabs(["1. 원본", "2. [Unnamed: 1] 삭제", "3. [Unnamed: 0] 변경"])
df = pd.read_html(url)[0].drop(0)
data1 = df.drop('Unnamed: 1', axis=1)
data2 = data1.iloc[::2,:].set_index(keys="Unnamed: 0")
with col1:
    st.dataframe(df)
with col2:
    st.dataframe(data1)
with col3:
    st.dataframe(data2)

def makeCol(data):
    point = []
    target = st.session_state.slider_value
    for i in range(target[0], target[1]+1):
        point.append(str(i))
    if len(point) == 0:
        point = list(data.columns)
    return point

sl = st.slider(
    label="년도 범위를 변경하세요",
    min_value=1989,
    max_value=2023,
    value=st.session_state.slider_value,
    step=1
)

if st.button("선택한 범위 확인"):
    st.session_state.slider_value = sl
    st.text(st.session_state.slider_value)
    data3 = data2.filter(items=makeCol(data2)).transpose()
    # st.dataframe(data3)
    # st.text( makeCol(data2) )
    tab3, tab4 = st.tabs(["데이터", "차트"])
    with tab3:
        st.dataframe(data3, use_container_width=True)
    with tab4:
        st.line_chart(data3)

    