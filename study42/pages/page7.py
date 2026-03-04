import streamlit as st
import ollama

st.set_page_config(
	page_title="6. 로컬 실시간 AI",
	page_icon="💗",
	layout="wide",
)

st.title("[6] 로컬 실시간 AI")

if "history" not in st.session_state:
  st.session_state["history"] = []

for msg in st.session_state["history"]:
  with st.chat_message(msg["role"]):
    st.write(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
  with st.chat_message("user"):
    st.write(prompt)

  st.session_state["history"].append({"role": "user", "content": prompt})

  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    stream = ollama.chat(
    #   model="gpt-oss:20b",
      model="gemma3:4b",
      messages=st.session_state["history"],
      stream=True
    )

    for chunk in stream:
        try:
            if "image_url" in chunk["message"]:
                st.image(url=chunk["message"]["image_url"], caption="이미지", width=400)
        except (KeyError, TypeError) as e:
            print(f"Error processing chunk: {e}")
            
        content = chunk["message"]["content"]
        full_response += content
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)

    st.session_state["history"].append({"role": "assistant", "content": full_response})

    