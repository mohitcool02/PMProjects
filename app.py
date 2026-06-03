import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("PM PRD Generator")

feature = st.text_input("Feature Name")
user = st.text_input("Target User")
problem = st.text_area("Problem Statement")
goal = st.text_area("Success Criteria")
actions = st.text_area("Key User Actions")
success = st.text_area("Success Metrics")

if st.button("Generate PRD"):

    prompt = f"""
You are a Senior Product Manager.

Create a PRD with:
1. Problem Statement
2. Goals and Success Metrics
3. User Stories and Use Cases
4. Requirements
5. Risks
6. Scope and Constraints
7. Assumptions
8. Open Questions

Feature: {feature}
User: {user}
Problem: {problem}
Goal: {goal}
Key User Actions: {actions}
Success Metrics: {success}

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
