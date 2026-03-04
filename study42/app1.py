import streamlit as st
import pandas as pd
from vega_datasets import data
from numpy.random import default_rng as rng
import altair as alt

st.set_page_config(page_title="0304")

st.title("[1] 차트 출력하기")

# 데이터
source1 = data.barley()
source2 = data.cars()
df = pd.DataFrame(rng(0).standard_normal((20,3)), columns=["a","b","c"])

st.header("1. DataFrame List")
data1, data2, data3 = st.tabs(["1. Vega Datasets - Barley", "2. Vega Datasets - Cars", "3. 난수 생성 - 20행 3열 배열"])
with data1:
    st.dataframe(source1,use_container_width=True)
with data2:
    st.dataframe(source2,use_container_width=True)
with data3:
    st.dataframe(df,use_container_width=True)

# 막대 차트
st.header("2. Bar Chart - Barley 데이터셋")
st.bar_chart(source1, x="year", y="yield", color="site", stack=False)

st.header("3. 난수 데이터 차트")
tab1, tab2 = st.tabs(["Line Chart - 난수 데이터셋", "Scatter Chart - 난수 데이터셋"])
with tab1:
    st.line_chart(df) # 라인 차트
with tab2:
    st.scatter_chart(df) # 도트 차트

# 분포도 차트
st.header("4. Altair Chart - Cars 데이터셋")
chart = alt.Chart(source2).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

tab3, tab4 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
with tab3:
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab4:
    st.altair_chart(chart, theme=None , use_container_width=True)