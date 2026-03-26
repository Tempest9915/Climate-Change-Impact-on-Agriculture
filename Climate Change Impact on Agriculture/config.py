"""
Configuration file for Climate & Agriculture Dashboard
Contains all constants, color mappings, and configuration settings
"""

# ─────────────────────────────────────────────────────────────────────────────
# DATA FILE
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = "Climate Change Impact on Agriculture.csv"
CLEANED_DATA_FILE = "Climate_Agriculture_Cleaned.csv"

# ─────────────────────────────────────────────────────────────────────────────
# NUMERIC COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
NUMERIC_COLUMNS = [
    "Year", "Average_Temperature_C", "Total_Precipitation_mm",
    "CO2_Emissions_MT", "Crop_Yield_MT_per_HA", "Extreme_Weather_Events",
    "Irrigation_Access_%", "Pesticide_Use_KG_per_HA",
    "Fertilizer_Use_KG_per_HA", "Soil_Health_Index",
    "Economic_Impact_Million_USD",
]

# ─────────────────────────────────────────────────────────────────────────────
# FEATURE MAPPINGS
# ─────────────────────────────────────────────────────────────────────────────
ISO_MAP = {
    "Argentina": "ARG", "Australia": "AUS", "Brazil": "BRA",
    "Canada": "CAN",    "China": "CHN",      "France": "FRA",
    "India": "IND",     "Nigeria": "NGA",    "Russia": "RUS",
    "USA": "USA",
}

INCOME_MAP = {
    "USA": "High Income",    "France": "High Income",
    "Australia": "High Income", "Canada": "High Income",
    "Russia": "Upper-Middle", "China": "Upper-Middle",
    "Brazil": "Upper-Middle", "Argentina": "Upper-Middle",
    "India": "Lower-Middle", "Nigeria": "Low Income",
}

INCOME_ORDER = ["High Income", "Upper-Middle", "Lower-Middle", "Low Income"]

# ─────────────────────────────────────────────────────────────────────────────
# COLOR SCHEMES
# ─────────────────────────────────────────────────────────────────────────────
COUNTRY_COLORS = {
    "Argentina": "#e74c3c", "Australia": "#3498db", "Brazil":   "#2ecc71",
    "Canada":    "#e67e22", "China":     "#c0392b", "France":   "#9b59b6",
    "India":     "#f39c12", "Nigeria":   "#1abc9c", "Russia":   "#34495e",
    "USA":       "#2980b9",
}

INCOME_COLORS = {
    "High Income":    "#ef4444",
    "Upper-Middle":   "#f97316",
    "Lower-Middle":   "#3b82f6",
    "Low Income":     "#94a3b8",
}

GREEN_SCALE = [
    [0.0, "#f0fdf4"], [0.25, "#86efac"],
    [0.5, "#22c55e"], [0.75, "#15803d"], [1.0, "#14532d"],
]

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY STYLING
# ─────────────────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#f9fafb",
    font=dict(family="'Inter', sans-serif", color="#374151", size=11),
    hovermode="closest",
    hoverlabel=dict(
        bgcolor="#ffffff",
        bordercolor="#1f2937",
        font=dict(color="#000000", size=12, family="'Inter', sans-serif"),
        namelength=-1,
        align="left",
    ),
    margin=dict(t=10, b=40, l=55, r=20),
)

AXIS_STYLE = dict(
    gridcolor="#e5e7eb",
    zerolinecolor="#d1d5db",
    tickfont=dict(color="#1f2937", size=10),
    title_font=dict(color="#1f2937", size=10),
    linecolor="#9ca3af",
)

# ─────────────────────────────────────────────────────────────────────────────
# CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
CORRELATION_COLUMNS = [
    "Average_Temperature_C", "Total_Precipitation_mm", "CO2_Emissions_MT",
    "Crop_Yield_MT_per_HA", "Extreme_Weather_Events",
    "Irrigation_Access_%", "Soil_Health_Index", "Economic_Impact_Million_USD",
]

CORRELATION_LABELS = [
    "Temp °C", "Precip mm", "CO₂ MT", "Yield MT/ha",
    "Extreme Events", "Irrigation %", "Soil Health", "Econ Impact"
]

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
MAX_SCATTER_SAMPLES = 2000