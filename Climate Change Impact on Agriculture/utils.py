"""
Utility functions for the Climate & Agriculture Dashboard
"""

import streamlit as st


def chart_panel(title, subtitle, tag_label, tag_class, fig, insight=None):
    """
    Display a chart in a styled panel with title, tag, and optional insight box
    
    Args:
        title (str): Chart title
        subtitle (str): Chart subtitle/description
        tag_label (str): Tag label (e.g., "Bar Chart", "Heatmap")
        tag_class (str): CSS class for tag styling (e.g., "tag-green", "tag-blue")
        fig (go.Figure): Plotly figure to display
        insight (str, optional): Insight/finding text (can include HTML/markdown). Defaults to None.
    """
    st.markdown(f"""
    <div class="chart-panel">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div class="chart-title">{title}</div>
          <div class="chart-sub">{subtitle}</div>
        </div>
        <span class="tag {tag_class}">{tag_label}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    if insight:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def display_title_banner():
    """Display the main title banner"""
    st.markdown("""
    <div class="title-banner">
      <h1>🌱 Climate Change Impact on Agriculture</h1>
      <p>Interactive Analytics Dashboard &nbsp;·&nbsp; Historical Analysis 1990–2024
         &nbsp;·&nbsp; 10 Countries &nbsp;·&nbsp;
         ITS68404 Data Visualization &nbsp;·&nbsp; Taylor's University 2026</p>
      <div class="sdg-row">
        <span class="sdg-pill">● SDG 2 – Zero Hunger</span>
        <span class="sdg-pill">● SDG 13 – Climate Action</span>
        <span class="sdg-pill">● SDG 10 – Reduced Inequalities</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def display_section_header(text):
    """Display a section header"""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def display_footer():
    """Display footer information"""
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:0.70rem;color:#9ca3af;
                padding:14px 0;border-top:1px solid #e5e7eb;letter-spacing:0.5px;">
      ITS68404 Data Visualization &nbsp;·&nbsp; Taylor's University &nbsp;·&nbsp;
      January 2026 Semester &nbsp;·&nbsp;
      Dataset: Climate Change Impact on Agriculture (1990–2024) &nbsp;·&nbsp;
      SDG 2: Zero Hunger &nbsp;·&nbsp; SDG 13: Climate Action
    </div>
    """, unsafe_allow_html=True)
