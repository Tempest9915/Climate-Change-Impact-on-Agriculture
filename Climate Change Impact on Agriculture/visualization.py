"""
Basic visualization functions for EDA charts
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import PLOTLY_LAYOUT, AXIS_STYLE, COUNTRY_COLORS
from utils import chart_panel


def create_multilayer_chart(temp_trend):
    """
    Create multi-layer chart: Crop Yield + Temperature + Extreme Events
    
    Args:
        temp_trend (pd.DataFrame): Annual trend data
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=temp_trend["Year"], y=temp_trend["Crop_Yield_MT_per_HA"],
        name="Crop Yield (MT/HA)",
        marker_color="rgba(34,197,94,0.55)",
        hovertemplate="<b>%{x}</b><br>Yield: %{y:.3f} MT/HA<extra></extra>",
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=temp_trend["Year"], y=temp_trend["Average_Temperature_C"],
        name="Avg Temp (°C)",
        mode="lines+markers",
        line=dict(color="#dc2626", width=2.2),
        marker=dict(size=4),
        hovertemplate="<b>%{x}</b><br>Temp: %{y:.2f}°C<extra></extra>",
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=temp_trend["Year"], y=temp_trend["Extreme_Weather_Events"],
        name="Extreme Events",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        marker=dict(size=4, symbol="triangle-up"),
        hovertemplate="<b>%{x}</b><br>Extreme Events: %{y:.2f}<extra></extra>",
    ), secondary_y=True)

    ml_layout = dict(PLOTLY_LAYOUT)
    ml_layout.update(dict(
        height=340,
        legend=dict(x=1.02, y=0.98, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#e5e7eb", borderwidth=1, font=dict(size=10)),
        margin=dict(t=10, b=40, l=55, r=100),
    ))
    fig.update_layout(**ml_layout)
    fig.update_xaxes(title_text="Year", **AXIS_STYLE)
    fig.update_yaxes(title_text="Crop Yield (MT/HA)",
                     title_font=dict(color="#16a34a", size=10),
                     tickfont=dict(color="#16a34a", size=10),
                     gridcolor="#f3f4f6", secondary_y=False)
    fig.update_yaxes(title_text="Temperature °C / Extreme Events",
                     title_font=dict(color="#dc2626", size=10),
                     tickfont=dict(color="#dc2626", size=10),
                     showgrid=False, secondary_y=True)
    
    return fig


def create_yield_by_crop_chart(yield_crop):
    """
    Create bar chart of average crop yield by crop type
    
    Args:
        yield_crop (pd.DataFrame): Crop type vs average yield
        
    Returns:
        go.Figure: Plotly figure
    """
    bar_colors = ["#14532d", "#166534", "#15803d", "#16a34a", "#22c55e",
                  "#4ade80", "#86efac", "#bbf7d0", "#dcfce7", "#f0fdf4"]
    mean_yield = float(yield_crop["Crop_Yield_MT_per_HA"].mean()) if not yield_crop.empty else 0
    
    fig = go.Figure(go.Bar(
        x=yield_crop["Crop_Type"],
        y=yield_crop["Crop_Yield_MT_per_HA"],
        marker_color=bar_colors[:len(yield_crop)],
        marker_opacity=0.88,
        text=yield_crop["Crop_Yield_MT_per_HA"].round(3),
        textposition="outside",
        textfont=dict(color="#9ca3af", size=9),
        hovertemplate="<b>%{x}</b><br>Yield: %{y:.3f} MT/HA<extra></extra>",
    ))
    
    fig.add_hline(y=mean_yield, line_dash="dot", line_color="#9ca3af",
                  line_width=1.2,
                  annotation_text=f"avg {mean_yield:.3f}",
                  annotation_font_size=9,
                  annotation_font_color="#9ca3af")
    
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=340,
        xaxis=dict(**AXIS_STYLE, showgrid=False, tickangle=-30),
        yaxis=dict(**AXIS_STYLE, title="Avg Yield (MT/HA)",
                   range=[0, yield_crop["Crop_Yield_MT_per_HA"].max() * 1.18]),
    )
    
    return fig


def create_scatter_chart(scatter_df):
    """
    Create scatter plot: Temperature vs Crop Yield
    
    Args:
        scatter_df (pd.DataFrame): Sampled scatter data
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = go.Figure()
    
    for country in scatter_df["Country"].unique() if not scatter_df.empty else []:
        sub = scatter_df[scatter_df["Country"] == country]
        fig.add_trace(go.Scatter(
            x=sub["Average_Temperature_C"], y=sub["Crop_Yield_MT_per_HA"],
            mode="markers", name=country,
            marker=dict(size=5, color=COUNTRY_COLORS.get(country, "#94a3b8"),
                        opacity=0.6),
            text=sub["Crop_Type"],
            hovertemplate=(f"<b>{country}</b><br>Crop: %{{text}}<br>"
                           "Temp: %{x}°C<br>Yield: %{y} MT/HA<extra></extra>"),
        ))
    
    if not scatter_df.empty:
        z = np.polyfit(scatter_df["Average_Temperature_C"],
                       scatter_df["Crop_Yield_MT_per_HA"], 1)
        xs = np.linspace(scatter_df["Average_Temperature_C"].min(),
                         scatter_df["Average_Temperature_C"].max(), 100)
        fig.add_trace(go.Scatter(
            x=xs, y=np.poly1d(z)(xs),
            mode="lines", name="Trend",
            line=dict(color="#1f2937", width=1.8, dash="dash"),
            hoverinfo="skip",
        ))
    
    sc_layout = dict(PLOTLY_LAYOUT)
    sc_layout.update(dict(
        height=340,
        xaxis=dict(**AXIS_STYLE, title="Average Temperature (°C)"),
        yaxis=dict(**AXIS_STYLE, title="Crop Yield (MT/HA)"),
        legend=dict(x=1.02, y=0.98, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#e5e7eb", borderwidth=1, font=dict(size=9)),
        margin=dict(t=10, b=40, l=55, r=100),
    ))
    fig.update_layout(**sc_layout)
    
    return fig


def create_boxplot_chart(dff):
    """
    Create box plot: Crop Yield by Adaptation Strategy
    
    Args:
        dff (pd.DataFrame): Filtered dataset
        
    Returns:
        go.Figure: Plotly figure
    """
    strat_colors = ["#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ef4444"]
    fig = go.Figure()
    
    adapt_clean = dff.dropna(subset=["Adaptation_Strategies"])
    for i, strat in enumerate(adapt_clean["Adaptation_Strategies"].unique()):
        vals = adapt_clean[adapt_clean["Adaptation_Strategies"] == strat][
            "Crop_Yield_MT_per_HA"
        ].dropna()
        fig.add_trace(go.Box(
            y=vals, name=strat,
            marker_color=strat_colors[i % len(strat_colors)],
            boxmean="sd",
            hovertemplate=f"<b>{strat}</b><br>Yield: %{{y:.3f}}<extra></extra>",
        ))
    
    fig.update_layout(
        **PLOTLY_LAYOUT, height=340,
        xaxis=dict(**AXIS_STYLE, showgrid=False),
        yaxis=dict(**AXIS_STYLE, title="Crop Yield (MT/HA)"),
        showlegend=False,
    )
    
    return fig
