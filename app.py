import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("PM PRD Generator")

# Form
with st.form("prd_form"):

    feature = st.text_input("Feature Name")
    target_user = st.text_input("Target User")
    problem = st.text_area("Problem Statement")

    col1, col2 = st.columns(2)

    analyze_btn = col1.form_submit_button("Analyze Requirements")
    generate_btn = col2.form_submit_button("Generate PRD")

# ANALYZE BUTTON
if analyze_btn:

    prompt = f"""
    Review this product idea.

    Feature: {feature}
    User: {target_user}
    Problem: {problem}

    Identify:
    1. Missing information
    2. Risks
    3. Edge cases
    4. Clarifying questions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Senior Product Manager."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    analysis = response.choices[0].message.content

    # Save for later use
    st.session_state["analysis"] = analysis

    st.subheader("Requirement Analysis")
    st.write(analysis)


# Show saved analysis even after reruns
if "analysis" in st.session_state:
    st.subheader("Latest Analysis")
    st.write(st.session_state["analysis"])


# GENERATE PRD BUTTON
if generate_btn:

 
You are a Principal Product Manager at a top technology company.

Generate a professional Product Requirements Document (PRD).

Instructions:
- Think like an experienced PM.
- Be specific and actionable.
- Avoid generic statements.
- Identify gaps and assumptions.
- Include realistic requirements.
- Use markdown formatting.

    Feature: {feature}
    User: {target_user}
    Problem: {problem}

    Requirement Analysis:
    {analysis}

    Include:

    # Executive Summary
    # Problem Statement
    # User Stories
    # Functional Requirements
    # Risks
    # Scope
    # Assumptions
    # Open Questions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Principal Product Manager."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    prd = response.choices[0].message.content

    st.subheader("Generated PRD")
    st.markdown(prd)

    st.download_button(
        "Download PRD",
        prd,
        file_name="prd.md",
        mime="text/markdown"
    )
