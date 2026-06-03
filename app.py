import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("PM PRD Generator")

feature = st.text_input("Feature Name")
user = st.text_input("Target User")
problem = st.text_area("Problem Statement")

if st.button("Generate PRD"):

    prompt = f"""
You are a Senior Product Manager.

Create a PRD with:
1. Problem Statement
2. Goals
3. User Stories
4. Requirements
5. Risks

Feature: {feature}
User: {user}
Problem: {problem}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a PM assistant"},
            {"role": "user", "content": prompt}
        ]
    )

    st.markdown("## Generated PRD")
    st.write(response.choices[0].message.content)
