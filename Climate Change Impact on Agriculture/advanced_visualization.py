"""
Advanced visualization functions for complex analytical charts
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
# Added make_subplots for the dual-axis line chart
from plotly.subplots import make_subplots 
from config import (
    PLOTLY_LAYOUT, AXIS_STYLE, COUNTRY_COLORS, 
    GREEN_SCALE, INCOME_COLORS, INCOME_ORDER, 
    CORRELATION_COLUMNS, CORRELATION_LABELS
)

def create_temp_co2_line_chart(dff):
    """
    Create a dual-axis line chart for Temperature and CO2 Emissions over time
    """
    # Aggregate data by year for the trend lines
    trend_data = dff.groupby("Year").agg({
        "Average_Temperature_C": "mean",
        "CO2_Emissions_MT": "mean"
    }).reset_index()

    # Initialize subplots with a secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Temperature Line (Left Axis)
    fig.add_trace(go.Scatter(
        x=trend_data["Year"], 
        y=trend_data["Average_Temperature_C"],
        name="Avg Temp (°C)",
        mode="lines+markers",
        line=dict(color="#dc2626", width=3), # Red for heat
        hovertemplate="Year: %{x}<br>Temp: %{y:.2f}°C<extra></extra>"
    ), secondary_y=False)

    # 2. CO2 Emissions Line (Right Axis)
    fig.add_trace(go.Scatter(
        x=trend_data["Year"], 
        y=trend_data["CO2_Emissions_MT"],
        name="CO2 Emissions (MT)",
        mode="lines+markers",
        line=dict(color="#4b5563", width=3, dash="dot"), # Slate for emissions
        hovertemplate="Year: %{x}<br>CO2: %{y:.2f} MT<extra></extra>"
    ), secondary_y=True)

    # Update layout using the project's standard configuration
    line_layout = dict(PLOTLY_LAYOUT)
    
    # Create axis styles with color overrides
    temp_axis_style = dict(AXIS_STYLE)
    temp_axis_style.update(dict(
        tickfont=dict(color="#dc2626", size=10),
        title_font=dict(color="#dc2626", size=10)
    ))
    
    co2_axis_style = dict(AXIS_STYLE)
    co2_axis_style.update(dict(
        tickfont=dict(color="#4b5563", size=10),
        title_font=dict(color="#4b5563", size=10)
    ))
    
    line_layout.update(dict(
        height=360,
        xaxis=dict(**AXIS_STYLE, title="Year"),
        yaxis=dict(
            **temp_axis_style, 
            title="Temperature (°C)"
        ),
        yaxis2=dict(
            **co2_axis_style, 
            title="CO2 Emissions (MT)",
            overlaying="y", 
            side="right",
            showgrid=False
        ),
        legend=dict(
            x=0.5, y=-0.25, 
            xanchor="center",
            yanchor="top",
            orientation="h",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e5e7eb", 
            borderwidth=1
        ),
        margin=dict(t=10, b=40, l=55, r=55),
    ))
    fig.update_layout(**line_layout)
    
    return fig

def create_stacked_area_chart(ew_pivot, dff):
    """
    Create stacked area chart for extreme weather events over time
    """
    fig = go.Figure()
    ew_countries = ew_pivot.columns.tolist()
    
    for i, country in enumerate(ew_countries):
        hex_col = list(COUNTRY_COLORS.values())[i % len(COUNTRY_COLORS)]
        r = int(hex_col[1:3], 16)
        g = int(hex_col[3:5], 16)
        b = int(hex_col[5:7], 16)
        
        fig.add_trace(go.Scatter(
            x=ew_pivot.index, y=ew_pivot[country],
            name=country, mode="lines",
            stackgroup="ew",
            fillcolor=f"rgba({r},{g},{b},0.72)",
            line=dict(width=0),
            hovertemplate=(f"<b>{country} %{{x}}</b><br>"
                           "Events: %{y:.2f}<extra></extra>"),
        ))
    
    area_layout = dict(PLOTLY_LAYOUT)
    area_layout.update(dict(
        height=320,
        xaxis=dict(**AXIS_STYLE, title="Year"),
        yaxis=dict(**AXIS_STYLE, title="Avg Extreme Events (stacked)"),
        legend=dict(x=1.02, y=0.98, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#e5e7eb", borderwidth=1, font=dict(size=9)),
        margin=dict(t=10, b=40, l=55, r=100),
    ))
    fig.update_layout(**area_layout)
    
    return fig

def create_heatmap_chart(dff):
    """
    Create heatmap: Country × Crop Type Yield
    """
    heat_pivot = (dff.groupby(["Country", "Crop_Type"])["Crop_Yield_MT_per_HA"]
                  .mean().round(3).unstack(fill_value=0))
    
    fig = go.Figure(go.Heatmap(
        z=heat_pivot.values.tolist(),
        x=heat_pivot.columns.tolist(),
        y=heat_pivot.index.tolist(),
        colorscale=GREEN_SCALE,
        showscale=True,
        colorbar=dict(title=dict(text="MT/HA", font=dict(size=10, color="#9ca3af")),
                      thickness=10, len=0.7,
                      tickfont=dict(size=9, color="#9ca3af")),
        text=[[f"{v:.2f}" for v in row] for row in heat_pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=9, color="#374151"),
        hovertemplate="<b>%{y}</b> – %{x}<br>Yield: %{z:.3f} MT/HA<extra></extra>",
    ))
    
    hm_layout = dict(PLOTLY_LAYOUT)
    hm_layout.update(dict(
        height=320,
        xaxis=dict(**AXIS_STYLE, showgrid=False, tickangle=-30),
        yaxis=dict(**AXIS_STYLE, showgrid=False),
        margin=dict(t=10, b=55, l=90, r=80),
    ))
    fig.update_layout(**hm_layout)
    
    return fig

def create_inequality_chart(dff):
    """
    Create grouped bar chart showing structural inequality by income group
    """
    group_summary = (dff.groupby("Income_Group").agg(
        avg_yield      = ("Crop_Yield_MT_per_HA", "mean"),
        avg_irrigation = ("Irrigation_Access_%",  "mean"),
        avg_soil       = ("Soil_Health_Index",     "mean"),
    ).reindex(INCOME_ORDER))
    
    bias_vals_yield = [
        float(group_summary.loc[g, "avg_yield"])
        if g in group_summary.index and not np.isnan(group_summary.loc[g, "avg_yield"])
        else 0 for g in INCOME_ORDER
    ]
    bias_vals_irrig = [
        float(group_summary.loc[g, "avg_irrigation"])
        if g in group_summary.index and not np.isnan(group_summary.loc[g, "avg_irrigation"])
        else 0 for g in INCOME_ORDER
    ]
    bias_colors_list = [INCOME_COLORS.get(g, "#94a3b8") for g in INCOME_ORDER]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Avg Yield (MT/HA)",
        x=INCOME_ORDER, y=bias_vals_yield,
        marker_color=bias_colors_list, marker_opacity=0.88,
        text=[f"{v:.2f}" for v in bias_vals_yield],
        textposition="outside",
        textfont=dict(color="#9ca3af", size=9),
        hovertemplate="<b>%{x}</b><br>Avg Yield: %{y:.2f} MT/HA<extra></extra>",
    ))
    
    fig.add_trace(go.Bar(
        name="Irrigation Access (%)",
        x=INCOME_ORDER, y=bias_vals_irrig,
        marker_color=bias_colors_list, marker_opacity=0.40,
        marker_pattern_shape="/",
        text=[f"{v:.1f}%" for v in bias_vals_irrig],
        textposition="outside",
        textfont=dict(color="#9ca3af", size=9),
        hovertemplate="<b>%{x}</b><br>Irrigation: %{y:.1f}%<extra></extra>",
    ))
    
    ineq_layout = dict(PLOTLY_LAYOUT)
    ineq_layout.update(dict(
        barmode="group", bargap=0.28,
        height=360,
        xaxis=dict(**AXIS_STYLE, showgrid=False, tickangle=-10),
        yaxis=dict(**AXIS_STYLE, title="Value"),
        legend=dict(x=1.02, y=0.98, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.92)",
                    bordercolor="#e5e7eb", borderwidth=1, font=dict(size=10)),
        margin=dict(t=10, b=40, l=55, r=115),
    ))
    fig.update_layout(**ineq_layout)
    
    return fig

def create_choropleth_map(dff):
    """
    Create choropleth map showing average crop yield by country with dynamic text labels
    """
    map_data = (dff.groupby(["Country", "ISO3"])
                .agg(avg_yield      = ("Crop_Yield_MT_per_HA",       "mean"),
                     avg_temp       = ("Average_Temperature_C",       "mean"),
                     avg_extreme    = ("Extreme_Weather_Events",      "mean"),
                     avg_co2        = ("CO2_Emissions_MT",            "mean"),
                     avg_irrigation = ("Irrigation_Access_%",         "mean"),
                     avg_soil       = ("Soil_Health_Index",           "mean"),
                     total_econ     = ("Economic_Impact_Million_USD", "sum"))
                .reset_index().round(3))
    
    country_coords = {
        "ARG": {"lon": -63.6, "lat": -38.4},
        "AUS": {"lon": 133.8, "lat": -27.0},
        "BRA": {"lon": -51.9, "lat": -14.2},
        "CAN": {"lon": -106.3, "lat": 56.1},
        "CHN": {"lon": 104.2, "lat": 35.9},
        "FRA": {"lon": 2.2, "lat": 46.2},
        "IND": {"lon": 78.9, "lat": 20.6},
        "NGA": {"lon": 8.7, "lat": 9.1},
        "RUS": {"lon": 105.3, "lat": 61.5},
        "USA": {"lon": -95.7, "lat": 37.1},
    }

    map_data['lon'] = map_data['ISO3'].map(lambda x: country_coords.get(x, {}).get('lon'))
    map_data['lat'] = map_data['ISO3'].map(lambda x: country_coords.get(x, {}).get('lat'))

    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        locations=map_data["ISO3"],
        z=map_data["avg_yield"],
        customdata=map_data["Country"],
        hovertemplate="%{customdata}<br>Yield: %{z:.3f} MT/HA<extra></extra>",
        colorscale=GREEN_SCALE,
        showscale=True,
        colorbar=dict(
            title=dict(text="Avg Crop Yield<br>(MT/HA)", font=dict(size=11)),
            thickness=14, len=0.55
        ),
        marker=dict(line=dict(color="#ffffff", width=1)),
    ))

    fig.add_trace(go.Scattergeo(
        lon=map_data["lon"],
        lat=map_data["lat"],
        text=map_data["Country"],
        mode="text",
        textfont=dict(
            family="'Inter', sans-serif",
            size=10,
            color="#1f2937",
        ),
        hoverinfo="skip" 
    ))

    map_layout = dict(
        height=500,
        margin=dict(t=10, b=10, l=0, r=80),
        geo=dict(
            projection=dict(type="natural earth"),
            showframe=False,
            showland=True, landcolor="#f1f5f9",
            showocean=True, oceancolor="#dbeafe",
            showlakes=True, lakecolor="#bfdbfe",
            lataxis=dict(range=[-60, 85]),
            lonaxis=dict(range=[-180, 180]),
        ),
    )

    fig.update_layout(**map_layout)
    
    return fig
