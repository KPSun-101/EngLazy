import streamlit as st
import os


import requests
import json
API_KEY = st.secrets["API_KEY"]

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngLazy!",
    page_icon="✍️",
    layout="centered"
)

# =========================
# TITLE
# =========================
st.markdown(
    "<h1 style='text-align: center;'>EngLazy!</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>Write Your Experience</h3>",
    unsafe_allow_html=True
)

# =========================
# TEXT INPUT
# =========================
text = st.text_area(
    "Write here:",
    height=250,
    placeholder="Write your daily experience in English..."
)

# =========================
# ANALYZE FUNCTION
# =========================
def analyze_text(user_text):

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "openai/gpt-oss-120b:free",

            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are an English Writing Analyzer(for who try to write/learn fluent English).

Analyze the following text carefully.

Tasks:
1. Always give same format result
2. Show corrected version(With improve sentence structure)
3. Give rating out of 20(average Grammar, Clarity, Spelling,Sentence flow)
4. Give scores for(Just score nothing more):
   - Grammar(out of 20 based on grammatical error)
   - Clarity(out of 20)
   - Spelling(out of 20)
   - Sentence flow(out of 20)
5.Simply explain errors(by a beautiful format)

Student Text:
{user_text}
"""
                }
            ],

            "max_tokens": 200
        })
    )

    return response.json()

# =========================
# BUTTON
# =========================
if st.button("Analyze My Writing"):

    if text.strip() == "":
        st.warning("Please write something first.")

    else:

        with st.spinner("Analyzing your writing..."):

            try:

                result = analyze_text(text)

                if "choices" in result:

                    ai_response = result['choices'][0]['message']['content']

                    st.markdown("## Feedback & Rating")
                    st.write(ai_response)

                else:
                    st.error(f"API Error:\n\n{result}")

            except Exception as e:
                st.error(f"Error:\n{e}")
