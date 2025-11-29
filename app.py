import streamlit as st
from langchain_helper import explain_code, generate_tests
import os
from datetime import datetime
import textwrap

# ---------- Page config ----------
st.set_page_config(
    page_title="Code Explainer & Test Generator",
    page_icon="🧠➡️🧪",
    layout="wide",
)

# ---------- CSS (small modern tweaks) ----------
st.markdown(
    """
    <style>
    .stApp { font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .header { display:flex; align-items:center; gap:12px; }
    .title { font-size:28px; font-weight:700; margin:0; }
    .subtitle { color: #6b7280; margin:0; font-size:13px; }
    .card { background: #ffffff; padding: 16px; border-radius: 10px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); }
    .small { font-size:12px; color:#6b7280; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
with st.container():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown(
            """
            <div class="header">
                <div style="font-size:36px">🧠➡️🧪</div>
                <div>
                    <div class="title">Code Explainer & Test Generator</div>
                    <div class="subtitle">Paste Python code, get concise explanations, refactors, and pytest stubs instantly.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- Sidebar: examples & history ----------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {time, code, explanation, tests}

st.sidebar.markdown("### ⚙️ Session")
if st.sidebar.button("Clear History"):
    st.session_state.history = []

st.sidebar.markdown("---")
st.sidebar.markdown("### Examples")
examples = {
    "Fibonacci (iterative)": textwrap.dedent(
        """
        def fib(n):
            if n < 0:
                raise ValueError("n must be >= 0")
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a
        """
    ),
    "Prime check": textwrap.dedent(
        """
        def is_prime(n):
            if n <= 1:
                return False
            if n <= 3:
                return True
            if n % 2 == 0 or n % 3 == 0:
                return False
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return False
                i += 6
            return True
        """
    ),
    "Simple Flask route": textwrap.dedent(
        """
        from flask import Flask, jsonify

        app = Flask(__name__)

        @app.route('/ping')
        def ping():
            return jsonify({'status': 'ok'})
        """
    ),
}
chosen_example = st.sidebar.selectbox("Load example", ["(none)"] + list(examples.keys()))
if chosen_example != "(none)":
    st.session_state.code_input = examples[chosen_example]

st.sidebar.markdown("---")
st.sidebar.markdown("### History (click to load)")
for i, item in enumerate(reversed(st.session_state.history[-20:])):
    t = item["time"]
    label = f"{t} — {item.get('summary','snippet')}"
    if st.sidebar.button(label, key=f"hist_{i}"):
        st.session_state.code_input = item["code"]
        st.session_state.last_explanation = item.get("explanation", "")
        st.session_state.last_tests = item.get("tests", "")

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ — paste code and press the buttons")

# ---------- Editor + Controls ----------
if "code_input" not in st.session_state:
    st.session_state.code_input = "# Paste your Python code here\n"

if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = ""
if "last_tests" not in st.session_state:
    st.session_state.last_tests = ""

editor_col, control_col = st.columns([3, 1])

with editor_col:
    st.markdown("**Code Editor**")
    code_input = st.text_area(
        "Paste code or upload a `.py` file",
        value=st.session_state.code_input,
        height=380,
        placeholder="# paste python code here..."
    )
    uploaded = st.file_uploader("Or upload a .py file", type=["py"])
    if uploaded:
        code_input = uploaded.read().decode("utf-8")
    st.session_state.code_input = code_input

with control_col:
    st.markdown("**Actions**")
    temperature = st.slider("LLM creativity", 0.0, 1.0, 0.0, 0.05)
    colA, colB = st.columns(2)
    with colA:
        explain_btn = st.button("Explain", use_container_width=True)
    with colB:
        tests_btn = st.button("Gen Tests", use_container_width=True)

    st.markdown("---")
    st.markdown("**Options**")
    model_choice = st.selectbox("Model", ("default",), index=0)  # kept for future
    st.markdown("---")
    st.markdown("**Quick actions**")
    if st.button("Save last tests to file"):
        if st.session_state.last_tests.strip():
            fname = f"generated_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(st.session_state.last_tests)
            st.success(f"Saved tests as {fname}")
        else:
            st.warning("No generated tests to save.")

    if st.button("Clear outputs"):
        st.session_state.last_explanation = ""
        st.session_state.last_tests = ""
        st.success("Cleared last outputs.")

# ---------- Execute LLM calls ----------
if explain_btn and code_input.strip():
    with st.spinner("Generating explanation..."):
        try:
            resp = explain_code(code_input, temperature=temperature)
            st.session_state.last_explanation = resp
            # add to history
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "code": code_input,
                "explanation": resp,
                "tests": st.session_state.last_tests,
                "summary": (code_input.strip().splitlines()[0][:60] + "...") if code_input.strip() else "snippet"
            })
            st.success("Explanation generated")
        except Exception as e:
            st.error(f"LLM call failed: {e}")

if tests_btn and code_input.strip():
    with st.spinner("Generating pytest stubs..."):
        try:
            tests = generate_tests(code_input, temperature=temperature)
            st.session_state.last_tests = tests
            # update history
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "code": code_input,
                "explanation": st.session_state.last_explanation,
                "tests": tests,
                "summary": (code_input.strip().splitlines()[0][:60] + "...") if code_input.strip() else "snippet"
            })
            st.success("Tests generated")
        except Exception as e:
            st.error(f"LLM call failed: {e}")

# ---------- Output area ----------
out_col1, out_col2 = st.columns([1.5, 1])

with out_col1:
    st.markdown("### Explanation")
    if st.session_state.last_explanation:
        st.code(st.session_state.last_explanation, language="json")
    else:
        st.info("No explanation yet — press **Explain** to generate one.")

with out_col2:
    st.markdown("### Generated Tests")
    if st.session_state.last_tests:
        st.code(st.session_state.last_tests, language="python")
        # Download button
        st.download_button(
            label="⬇️ Download tests (.py)",
            data=st.session_state.last_tests,
            file_name=f"generated_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
            mime="text/x-python"
        )
    else:
        st.info("No tests yet — press **Gen Tests** to generate pytest stubs.")

# ---------- Footer ----------
st.markdown("---")
st.markdown("Tips: Try small functions first. If the code references third-party libraries, include minimal context at top of the editor.")
