"""
app/main.py — Streamlit entry point for the AI Data Analyst application.

Run with:   streamlit run app/main.py
"""

import sys
import os

# Ensure app/ is on the path so relative imports work when launched from repo root
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from config import APP_TITLE, APP_ICON, APP_DESCRIPTION
from analysis.data_loader import load_csv, get_preview
from agents.analyst_agent import AnalystAgent


# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — clean, professional dark-accented theme ──────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stFileUploader label { color: #94a3b8 !important; }

    /* Main background */
    .main { background: #f8fafc; }

    /* Section card */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,.07), 0 4px 16px rgba(0,0,0,.04);
        border: 1px solid #e2e8f0;
    }

    /* Insight block */
    .insight-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        color: #e2e8f0;
        border-radius: 12px;
        padding: 1.8rem 2.2rem;
        font-size: 0.97rem;
        line-height: 1.75;
        border-left: 4px solid #3b82f6;
        font-family: 'DM Sans', sans-serif;
    }
    .insight-box strong, .insight-box b { color: #93c5fd; }
    .insight-box ul { margin-top: 0.4rem; }
    .insight-box li { margin-bottom: 0.3rem; }

    /* Stat metric */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,.05);
    }
    .metric-label { font-size: 0.78rem; color: #64748b; text-transform: uppercase; letter-spacing: .05em; }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #1e293b; margin-top: .1rem; }

    /* Section header */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        border-radius: 999px;
        padding: .15rem .65rem;
        font-size: .75rem;
        font-weight: 600;
        border: 1px solid #bfdbfe;
        margin-left: .4rem;
    }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.markdown(f"<p style='color:#94a3b8;font-size:.88rem'>{APP_DESCRIPTION}</p>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"],
        help="Drop any CSV file — the agent handles the rest.",
    )

    st.markdown("---")
    st.markdown("**Try the sample dataset:**")
    use_sample = st.button("📂 Load Sample Sales Data", use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<p style='color:#475569;font-size:.78rem'>"
        "Powered by <b>Groq LLaMA 3 70B</b><br>"
        "Built with Streamlit · Pandas · Seaborn"
        "</p>",
        unsafe_allow_html=True,
    )


# ── Load data ─────────────────────────────────────────────────────────────────
df: pd.DataFrame | None = None

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_sales.csv")

if use_sample:
    try:
        df = load_csv(SAMPLE_PATH)
        st.session_state["df"] = df
    except Exception as e:
        st.error(f"Could not load sample data: {e}")

if uploaded_file is not None:
    try:
        df = load_csv(uploaded_file)
        st.session_state["df"] = df
    except ValueError as e:
        st.sidebar.error(str(e))

# Persist dataframe across reruns
if df is None and "df" in st.session_state:
    df = st.session_state["df"]


# ── Landing state (no data yet) ───────────────────────────────────────────────
if df is None:
    st.markdown(
        f"""
        <div style="text-align:center;padding:4rem 2rem;">
            <div style="font-size:4rem">📊</div>
            <h1 style="font-size:2.2rem;font-weight:800;color:#1e293b;margin:.5rem 0">{APP_TITLE}</h1>
            <p style="color:#64748b;font-size:1.05rem;max-width:520px;margin:0 auto 2rem">
                {APP_DESCRIPTION}
            </p>
            <p style="color:#94a3b8;font-size:.9rem">
                ← Upload a CSV or load the sample dataset from the sidebar to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ── Dataset is loaded — build the agent ──────────────────────────────────────
try:
    agent = AnalystAgent(df)
except EnvironmentError as e:
    st.error(f"🔑 {e}")
    st.info(
        "Create a `.env` file in the project root with:\n\n"
        "```\nGROQ_API_KEY=your_api_key_here\n```\n\n"
        "Get your free key at https://console.groq.com"
    )
    st.stop()


# ── Section 1: Quick stats ────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">🗃️ Dataset Overview</div>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Rows</div>'
        f'<div class="metric-value">{len(df):,}</div></div>',
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Columns</div>'
        f'<div class="metric-value">{df.shape[1]}</div></div>',
        unsafe_allow_html=True,
    )
with col_c:
    missing_pct = round(df.isnull().mean().mean() * 100, 1)
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Missing Values</div>'
        f'<div class="metric-value">{missing_pct}%</div></div>',
        unsafe_allow_html=True,
    )
with col_d:
    num_count = len(df.select_dtypes(include="number").columns)
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Numeric Cols</div>'
        f'<div class="metric-value">{num_count}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Dataset preview table
with st.expander("🔍 Preview Dataset (first 10 rows)", expanded=True):
    st.dataframe(get_preview(df, 10), use_container_width=True)

# Descriptive statistics table
with st.expander("📐 Descriptive Statistics"):
    stats_df = agent.get_descriptive_stats()
    if not stats_df.empty:
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.info("No numeric columns found for statistics.")

# Category breakdowns
cat_stats = agent.get_category_stats()
if cat_stats:
    with st.expander("🏷️ Categorical Breakdowns"):
        cols = st.columns(min(len(cat_stats), 3))
        for idx, (col_name, counts_df) in enumerate(cat_stats.items()):
            with cols[idx % len(cols)]:
                st.markdown(f"**{col_name.title()}**")
                st.dataframe(counts_df, use_container_width=True, hide_index=True)


# ── Section 2: Charts ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">📈 Visual Analysis</div>', unsafe_allow_html=True)

with st.spinner("Generating charts…"):
    charts = agent.generate_charts()

if not charts:
    st.warning("No charts could be generated from this dataset's structure.")
else:
    for title, fig in charts.items():
        st.markdown(f"<p class='section-header'>{title}</p>", unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ── Section 3: AI Insights ────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">🤖 AI Insights <span class="badge">Groq · LLaMA 3 70B</span></div>', unsafe_allow_html=True)

generate_btn = st.button("✨ Generate AI Insights", type="primary", use_container_width=False)

if generate_btn or "ai_insights" in st.session_state:
    if generate_btn:
        with st.spinner("Analysing data patterns with LLaMA 3 70B…"):
            try:
                insights = agent.generate_insights()
                st.session_state["ai_insights"] = insights
            except Exception as e:
                st.error(f"LLM error: {e}")
                st.stop()

    if "ai_insights" in st.session_state:
        st.markdown(
            f'<div class="insight-box">{st.session_state["ai_insights"]}</div>',
            unsafe_allow_html=True,
        )

        st.download_button(
            label="⬇️ Download Insights as TXT",
            data=st.session_state["ai_insights"],
            file_name="ai_insights.txt",
            mime="text/plain",
        )
else:
    st.info("Click **Generate AI Insights** to run the LLM analysis on your dataset.")
