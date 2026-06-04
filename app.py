import streamlit as st
from openai import OpenAI

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="PM PRD Generator", page_icon="📋", layout="centered")
st.title("📋 PM PRD Generator")
st.caption("Analyze requirements → Generate a production-ready PRD")

# ── Client ───────────────────────────────────────────────────────────────────
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = "You are a Principal Product Manager at a top-tier technology company."

# ── Input form ───────────────────────────────────────────────────────────────
with st.form("prd_form"):
    feature      = st.text_input("Feature Name", placeholder="e.g. In-app Notification Center")
    target_user  = st.text_input("Target User",  placeholder="e.g. B2B SaaS power users")
    problem      = st.text_area("Problem Statement", height=120,
                                placeholder="Describe the core problem this feature solves…")
    priority     = st.selectbox("Scope / Priority", ["MVP", "Execution", "Future Vision"])

    col1, col2 = st.columns(2)
    analyze_btn  = col1.form_submit_button("🔍 Analyze Requirements")
    generate_btn = col2.form_submit_button("📄 Generate PRD")

# ── Input validation helper ───────────────────────────────────────────────────
def inputs_valid():
    if not feature.strip() or not target_user.strip() or not problem.strip():
        st.warning("⚠️ Please fill in Feature Name, Target User, and Problem Statement.")
        return False
    return True

# ── API call helper ───────────────────────────────────────────────────────────
def call_openai(prompt: str, model: str = "gpt-4o-mini") -> str | None:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# ── ANALYZE ───────────────────────────────────────────────────────────────────
if analyze_btn:
    if inputs_valid():
        prompt = f"""
Review this product idea and return structured feedback.

Feature: {feature}
Target User: {target_user}
Problem: {problem}
Priority / Scope: {priority}

Identify:
1. Missing information that would strengthen the PRD
2. Key risks (technical, product, adoption)
3. Edge cases to consider
4. Clarifying questions the PM should answer before writing requirements

Be concise and specific. Avoid generic advice.
"""
        with st.spinner("Analyzing requirements…"):
            analysis = call_openai(prompt, model="gpt-4o-mini")

        if analysis:
            st.session_state["analysis"] = analysis

# Show analysis (persists across reruns, shown once)
if "analysis" in st.session_state:
    with st.expander("🔍 Requirement Analysis", expanded=True):
        st.write(st.session_state["analysis"])

# ── GENERATE PRD ──────────────────────────────────────────────────────────────
if generate_btn:
    if inputs_valid():
        # Silently run analysis first if not already done
        if "analysis" not in st.session_state:
            analyze_prompt = f"""
Feature: {feature} | User: {target_user} | Problem: {problem}
Briefly identify missing info, risks, edge cases, and open questions.
"""
            with st.spinner("Running quick analysis before generating PRD…"):
                analysis = call_openai(analyze_prompt, model="gpt-4o-mini")
            if analysis:
                st.session_state["analysis"] = analysis

        analysis = st.session_state.get("analysis", "None available.")

        prompt = f"""
Generate a professional, detailed Product Requirements Document (PRD).

Instructions:
- Be specific and actionable — no generic filler.
- Each section must have 3–5 bullet points minimum.
- Functional Requirements must include clear acceptance criteria.
- Flag assumptions explicitly.
- Use clean markdown formatting.

Inputs:
Feature: {feature}
Target User: {target_user}
Problem: {problem}
Priority / Scope: {priority}
Requirement Analysis: {analysis}

Structure the PRD with exactly these sections:
# Executive Summary
# Problem Statement
# Goals & Success Metrics
# User Stories
# Functional Requirements (with acceptance criteria)
# Non-Functional Requirements
# Out of Scope
# Risks & Mitigations
# Assumptions
# Open Questions
"""
        with st.spinner("Generating PRD… this may take 15–20 seconds"):
            prd = call_openai(prompt, model="gpt-4o")

        if prd:
            st.session_state["prd"] = prd

# Show PRD (persists across reruns)
if "prd" in st.session_state:
    st.divider()
    st.subheader("📄 Generated PRD")
    st.markdown(st.session_state["prd"])

    col_a, col_b = st.columns(2)
    col_a.download_button(
        label="⬇️ Download as Markdown",
        data=st.session_state["prd"],
        file_name=f"PRD_{feature.replace(' ', '_')}.md",
        mime="text/markdown",
    )
    if col_b.button("🔄 Reset & Start Over"):
        for key in ["analysis", "prd"]:
            st.session_state.pop(key, None)
        st.rerun()
