import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="PKS AI Chatbot")
st.title("🤖 PKS AI Chatbot")
st.write("Powered by xAI & Grok")

if "XAI_API_KEY" in st.secrets:
    xai_api_key = st.secrets["XAI_API_KEY"]
else:
    st.error("XAI_API_KEY is missing from Streamlit secrets.")
    st.stop()

client = OpenAI(
    api_key=xai_api_key,
    base_url="https://api.x.ai/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Grok anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="grok-3-mini",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"API Error: {e}")
