"""
Key Performance Indicator (KPI) calculations module
"""

def calculate_kpis(dff):
    """
    Calculate key metrics from filtered dataset
    
    Args:
        dff (pd.DataFrame): Filtered dataset
        
    Returns:
        dict: Dictionary containing all KPIs
    """
    return {
        "records": len(dff),
        "avg_temp": round(dff["Average_Temperature_C"].mean(), 2) if not dff.empty else 0,
        "avg_yield": round(dff["Crop_Yield_MT_per_HA"].mean(), 2) if not dff.empty else 0,
        "econ_impact": round(dff["Economic_Impact_Million_USD"].sum() / 1e6, 2) if not dff.empty else 0,
        "avg_co2": round(dff["CO2_Emissions_MT"].mean(), 2) if not dff.empty else 0,
        "avg_extreme": round(dff["Extreme_Weather_Events"].mean(), 1) if not dff.empty else 0,
        "num_countries": dff["Country"].nunique() if not dff.empty else 0,
    }


def display_kpi_cards(kpis):
    """
    Display KPI cards in Streamlit dashboard with enhanced styling and descriptions
    
    Args:
        kpis (dict): Dictionary of KPI values
    """
    import streamlit as st
    
    st.markdown("""
    <style>
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid var(--accent);
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
    }
    
    .kpi-sub {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 6px;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card" style="--accent:#16a34a">
        <div class="kpi-label"> Countries</div>
        <div class="kpi-value">{kpis["num_countries"]}</div>
        <div class="kpi-sub">Nations in selection</div>
      </div>
      <div class="kpi-card" style="--accent:#dc2626">
        <div class="kpi-label"> Avg Temperature</div>
        <div class="kpi-value">{kpis["avg_temp"]}°C</div>
        <div class="kpi-sub">Global farm avg</div>
      </div>
      <div class="kpi-card" style="--accent:#d97706">
        <div class="kpi-label"> Avg Crop Yield</div>
        <div class="kpi-value">{kpis["avg_yield"]}</div>
        <div class="kpi-sub">MT per hectare</div>
      </div>
      <div class="kpi-card" style="--accent:#7c3aed">
        <div class="kpi-label"> Econ Impact</div>
        <div class="kpi-value">${kpis["econ_impact"]}T</div>
        <div class="kpi-sub">Trillion USD total</div>
      </div>
      <div class="kpi-card" style="--accent:#64748b">
        <div class="kpi-label"> Avg CO₂ (MT)</div>
        <div class="kpi-value">{kpis["avg_co2"]}</div>
        <div class="kpi-sub">Per observation</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
