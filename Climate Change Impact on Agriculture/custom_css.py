"""
Custom CSS styling for the Climate & Agriculture Dashboard
"""

CUSTOM_CSS = """
<style>
/* ── Global ── */
[data-testid="stAppViewContainer"] {
    background: #f0f4f0;
}
[data-testid="stSidebar"] {
    background: #1a3a1a;
}
[data-testid="stSidebar"] * {
    color: #d4edda !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #a8d5a2 !important;
}
/* ── Title Banner ── */
.title-banner {
    background: linear-gradient(135deg, #14532d 0%, #166534 55%, #15803d 100%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 8px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.18);
}
.title-banner h1 {
    color: #ffffff;
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 0 0 6px 0;
    line-height: 1.2;
}
.title-banner p {
    color: rgba(255,255,255,0.72);
    font-size: 0.82rem;
    margin: 0;
    line-height: 1.5;
}
.sdg-row {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
}
.sdg-pill {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.35);
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 20px;
    letter-spacing: 0.4px;
}
/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 4px;
}
.kpi-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 14px 16px;
    border-top: 3px solid var(--accent);
    box-shadow: 0 1px 5px rgba(0,0,0,0.07);
    text-align: left;
}
.kpi-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    color: #7a9a7a;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.65rem;
    color: #a0b8a0;
    margin-top: 3px;
}
/* ── Section Headers ── */
.section-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a7c59;
    border-bottom: 2px solid #d1fae5;
    padding-bottom: 6px;
    margin: 16px 0 12px 0;
}
/* ── Insight Boxes ── */
.insight-box {
    background: #f9fafb;
    border-left: 3px solid #22c55e;
    border-radius: 0 6px 6px 0;
    padding: 9px 13px;
    font-size: 0.76rem;
    color: #1f2937;
    line-height: 1.6;
    margin-top: 8px;
}
.insight-box b { color: #000000; }
/* ── Chart Panels ── */
.chart-panel {
    background: #ffffff;
    border-radius: 8px;
    padding: 16px 18px 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-bottom: 12px;
}
.chart-title {
    font-size: 0.83rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 2px;
}
.chart-sub {
    font-size: 0.68rem;
    color: #9ca3af;
    margin-bottom: 10px;
}
/* ── Tags ── */
.tag {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 2px 9px;
    border-radius: 4px;
    letter-spacing: 0.3px;
    float: right;
}
.tag-green  { background:#f0fdf4; color:#166534; border:1px solid #bbf7d0; }
.tag-red    { background:#fef2f2; color:#991b1b; border:1px solid #fecaca; }
.tag-blue   { background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; }
.tag-amber  { background:#fffbeb; color:#92400e; border:1px solid #fde68a; }
.tag-purple { background:#f5f3ff; color:#5b21b6; border:1px solid #ddd6fe; }
.tag-teal   { background:#f0fdfa; color:#115e59; border:1px solid #99f6e4; }
/* ── Tooltip CSS ── */

/* 1. Target the SVG text elements specifically */
.js-plotly-plot .hoverlayer text {
    fill: #1f2937 !important; /* Force dark text color */
    stroke: none !important;
}

/* 2. Target the tooltip background box */
.js-plotly-plot .hoverlabel path {
    fill: #ffffff !important;
    fill-opacity: 1 !important;
    stroke: #d1d5db !important;
    stroke-width: 1px !important;
}

/* 3. Prevent sidebar styles from leaking into tooltips */
[data-testid="stSidebar"] .hoverlayer text {
    color: #1f2937 !important;
    fill: #1f2937 !important;
}
</style>
"""

def apply_custom_css():
    """Apply custom CSS to Streamlit app"""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)