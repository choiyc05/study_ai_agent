import streamlit as st
import trafilatura as tra
import ollama
import re

st.set_page_config(
	page_title="4. 뉴스기사 수집",
	page_icon="💗",
	layout="wide",
)

st.title("[4] 뉴스기사 수집")

def extract_txt_image(url: str):
    html = tra.fetch_url(url)
    text = tra.extract(html, output_format="markdown", include_comments=False)
    image = tra.extract_metadata(html).image
    return text, image

# 예시 : https://www.koreaherald.com/article/10685727
# 예시 : https://m.sports.naver.com/esports/article/015/0005057943?sid3=79b
if url := st.text_input("주소 입력", placeholder="URL을 입력하세요"):
    text, image = extract_txt_image(url)
    message = ""
    st.image(image)
    if re.search('[ㄱ-ㅎㅏ-ㅣ가-힣]', text):
        st.markdown(message)
    else:
        message_placeholder = st.empty()
        prompt = f"다음 영어 기사를 한글로 번역해주세요:\n {text}"
        stream = ollama.chat(
            # model="gpt-oss:20b",
            model="gemma3:4b",
            messages=[{"role":"user", "content": prompt}],
            stream = True
        )
        full_response = ""
        for chunk in stream:
            content = chunk["message"]["content"]
            full_response += content
            message_placeholder.markdown(full_response + "▌")
        # message = ollama.chat(model="gpt-oss:20b", messages=[{"role":"user","content": prompt}])
        # st.markdown(message)