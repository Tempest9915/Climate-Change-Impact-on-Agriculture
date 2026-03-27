import warnings
import streamlit as st
import pandas as pd

# Import custom modules
from config import MAX_SCATTER_SAMPLES
from custom_css import apply_custom_css
from data_preparation import load_and_clean, get_sidebar_filters, apply_filters
from kpi import calculate_kpis, display_kpi_cards
from utils import display_title_banner, display_section_header, chart_panel, display_footer
from visualization import (
    create_multilayer_chart, create_yield_by_crop_chart, 
    create_scatter_chart, create_boxplot_chart
)
from advanced_visualization import (
    create_stacked_area_chart, create_heatmap_chart,
    create_inequality_chart, create_choropleth_map, 
    create_temp_co2_line_chart
)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG 
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate & Agriculture Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# APPLY CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
apply_custom_css()

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
df = load_and_clean()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
sel_countries, sel_crops, sel_years, sel_strats = get_sidebar_filters(df)

# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS TO DATA
# ─────────────────────────────────────────────────────────────────────────────
dff = apply_filters(df, sel_countries, sel_crops, sel_years, sel_strats)

# Check if filtered data is empty
if dff.empty:
    st.error(" No data matches your filter selection. Please adjust your filters.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PREPARE DERIVED DATA FOR VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────────────────

# Trend data (annual averages)
temp_trend = (dff.groupby("Year")[
    ["Average_Temperature_C", "CO2_Emissions_MT",
     "Crop_Yield_MT_per_HA", "Extreme_Weather_Events"]
].mean().reset_index())

# Crop yield by type
yield_crop = (dff.groupby("Crop_Type")["Crop_Yield_MT_per_HA"]
              .mean().reset_index()
              .sort_values("Crop_Yield_MT_per_HA", ascending=False))

# Scatter sample (with proper sampling logic)
scatter_data_clean = dff[["Average_Temperature_C", "Crop_Yield_MT_per_HA",
                          "Country", "Crop_Type"]].dropna()
sample_size = min(MAX_SCATTER_SAMPLES, len(scatter_data_clean)) if len(scatter_data_clean) > 0 else 0
scatter_df = (scatter_data_clean.sample(n=sample_size, random_state=42)
              if sample_size > 0 else pd.DataFrame())

# Extreme weather pivot
ew_pivot = (dff.groupby(["Year", "Country"])["Extreme_Weather_Events"]
            .mean().unstack(fill_value=0))

# CALCULATE KPIs
kpis = calculate_kpis(dff)

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# Title Banner
display_title_banner()

# KPI Cards
display_kpi_cards(kpis)
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# SECTION A – TRENDS
display_section_header("A &nbsp;·&nbsp; Climate & Yield Trends")

col_a1, col_a2 = st.columns([2, 1])

with col_a1:
    fig_ml = create_multilayer_chart(temp_trend)
    chart_panel(
        title="Multi-Layer: Crop Yield · Temperature · Extreme Events",
        subtitle="",
        tag_label="Multi-Layer",
        tag_class="tag-blue",
        fig=fig_ml,
    )

with col_a2:
    fig_yb = create_yield_by_crop_chart(yield_crop)
    chart_panel(
        title="Avg Crop Yield by Crop Type",
        subtitle="",
        tag_label="Bar Chart",
        tag_class="tag-green",
        fig=fig_yb,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION B – RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
display_section_header("B &nbsp;·&nbsp; Relationships & Distributions")

col_b1, col_b2 = st.columns(2)

with col_b1:
    fig_sc = create_scatter_chart(scatter_df)
    chart_panel(
        title="Temperature vs Crop Yield by Country",
        subtitle="",
        tag_label="Scatter",
        tag_class="tag-blue",
        fig=fig_sc,
    )

with col_b2:
    fig_bp = create_boxplot_chart(dff)
    chart_panel(
        title="Crop Yield Distribution by Adaptation Strategy",
        subtitle="",
        tag_label="Box Plot",
        tag_class="tag-amber",
        fig=fig_bp,
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION C – PATTERNS OVER TIME
# ══════════════════════════════════════════════════════════════════════════════
display_section_header("C &nbsp;·&nbsp; Patterns Over Time")

col_c1, col_c2 = st.columns(2)

with col_c1:
    fig_ew = create_stacked_area_chart(ew_pivot, dff)
    chart_panel(
        title="Extreme Weather Events Over Time",
        subtitle="",
        tag_label="Stacked Area",
        tag_class="tag-red",
        fig=fig_ew,
    )

with col_c2:
    fig_hm = create_heatmap_chart(dff)
    chart_panel(
        title="Crop Yield Heatmap — Country × Crop Type",
        subtitle="",
        tag_label="Heatmap",
        tag_class="tag-green",
        fig=fig_hm,
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION D – CORRELATION & BIAS
# ══════════════════════════════════════════════════════════════════════════════
display_section_header("D &nbsp;·&nbsp; Trend Chart & Structural Inequality")

col_d1, col_d2 = st.columns(2)

with col_d1:
    # Use the new line chart function
    fig_temp_co2 = create_temp_co2_line_chart(dff) 
    chart_panel(
        title="Temperature & CO2 Emission Trends",
        subtitle="",
        tag_label="Line Chart",
        tag_class="tag-red",
        fig=fig_temp_co2,
    )

with col_d2:
    fig_bias = create_inequality_chart(dff)
    chart_panel(
        title="Structural Inequality — Resources by Income Group",
        subtitle="",
        tag_label="Ethical Bias",
        tag_class="tag-red",
        fig=fig_bias,
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION E – CHOROPLETH MAP
# ══════════════════════════════════════════════════════════════════════════════
display_section_header("E &nbsp;·&nbsp; Global View — Avg Crop Yield by Country")

fig_map = create_choropleth_map(dff)
chart_panel(
    title="Avg Crop Yield by Country (MT/HA)",
    subtitle="",
    tag_label="Choropleth Map",
    tag_class="tag-teal",
    fig=fig_map,
)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
display_footer()
