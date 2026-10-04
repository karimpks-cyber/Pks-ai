import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="PKS AI Chatbot", page_icon="🤖")

st.title("🤖 PKS AI Chatbot")
st.write("Powered by xAI & Grok")

# Initialize the xAI client using the secret stored in Streamlit
if "XAI_API_KEY" in st.secrets:
    xai_api_key = st.secrets["XAI_API_KEY"]
else:
    st.error("XAI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client with xAI's base URL
client = OpenAI(
    api_key=xai_api_key,
    base_url="https://api.x.ai/v1",
)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input from the chat box
if prompt := st.chat_input("Ask Grok anything..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Grok
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="grok-beta",  # Or your preferred Grok model
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.error(f"API Error: {e}")
