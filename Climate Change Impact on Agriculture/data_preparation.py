"""
Data loading, cleaning, and preprocessing module
"""

import pandas as pd
import numpy as np
import streamlit as st
from config import DATA_FILE, CLEANED_DATA_FILE, NUMERIC_COLUMNS, ISO_MAP, INCOME_MAP

@st.cache_data
def load_and_clean():
    """
    Load raw CSV, clean data, impute missing values with estimated means,
    add features, and save cleaned version.
    """
    # 1. Load raw data
    df_raw = pd.read_csv(DATA_FILE)

    # 2. Basic Cleaning: Strip whitespace and handle string 'nan'
    for col in df_raw.columns:
        df_raw[col] = df_raw[col].astype(str).str.strip()
        df_raw[col] = df_raw[col].replace("nan", np.nan).replace("", np.nan)

    # 3. Numeric Conversion
    for col in NUMERIC_COLUMNS:
        df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce")

    # 4. Filter Critical Identifiers
    # We drop rows where we don't know the Country, Year, or Crop because 
    # we cannot accurately "estimate" values without these anchors.
    df = df_raw.dropna(subset=["Year", "Country", "Crop_Type"]).copy()
    df["Year"] = df["Year"].astype(int)

    # 5. DATA IMPUTATION (Estimation of Nulls)
    # Define columns that need estimated values (exclude identifiers)
    impute_cols = [c for c in NUMERIC_COLUMNS if c not in ["Year"]]
    
    for col in impute_cols:
        # Step A: Estimate based on Country + Crop Type (Most accurate)
        df[col] = df[col].fillna(df.groupby(["Country", "Crop_Type"])[col].transform("mean"))
        
        # Step B: Estimate based on Country only (If Step A still leaves nulls)
        df[col] = df[col].fillna(df.groupby("Country")[col].transform("mean"))
        
        # Step C: Fallback to global mean (If a country has no data for that metric)
        df[col] = df[col].fillna(df[col].mean())

    # 6. Categorical Imputation
    if "Adaptation_Strategies" in df.columns:
        df["Adaptation_Strategies"] = df["Adaptation_Strategies"].fillna("Not Specified")
    
    if "Region" in df.columns:
        df["Region"] = df["Region"].fillna("Other")

    # 7. Feature engineering
    df["ISO3"] = df["Country"].map(ISO_MAP)
    df["Income_Group"] = df["Country"].map(INCOME_MAP)

    # 8. Save cleaned CSV
    df.to_csv(CLEANED_DATA_FILE, index=False)
    return df


def get_sidebar_filters(df):
    """
    Create sidebar filter controls with explanations and return selected values
    
    Args:
        df (DataFrame): Cleaned data to extract filter options from
    
    Returns:
        tuple: (countries, crops, years, strategies) selected by user
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("###  Filters")
    st.sidebar.markdown("", unsafe_allow_html=True)
    
    # Country multiselect
    countries = sorted(df["Country"].unique())
    st.sidebar.markdown("  Countries")
    st.sidebar.markdown("", unsafe_allow_html=True)
    selected_countries = st.sidebar.multiselect(
        " Countries",
        countries,
        default=countries,
        key="country_filter",
        label_visibility="collapsed"
    )
    
    # Crop type multiselect
    crops = sorted(df["Crop_Type"].unique())
    st.sidebar.markdown(" Crop Types")
    st.sidebar.markdown("", unsafe_allow_html=True)
    selected_crops = st.sidebar.multiselect(
        " Crop Types",
        crops,
        default=crops,
        key="crop_filter",
        label_visibility="collapsed"
    )
    
    # Year range slider
    years = sorted(df["Year"].unique())
    st.sidebar.markdown(" Time Period")
    st.sidebar.markdown("", unsafe_allow_html=True)
    year_range = st.sidebar.slider(
        " Year Range",
        min_value=int(years[0]),
        max_value=int(years[-1]),
        value=(int(years[0]), int(years[-1])),
        key="year_filter",
        label_visibility="collapsed"
    )
    
    # Adaptation strategy multiselect
    strategies = sorted(df["Adaptation_Strategies"].dropna().unique())
    st.sidebar.markdown(" Adaptation Strategies")
    st.sidebar.markdown("", unsafe_allow_html=True)
    selected_strategies = st.sidebar.multiselect(
        " Adaptation Strategies",
        strategies,
        default=strategies,
        key="strategy_filter",
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    return selected_countries, selected_crops, year_range, selected_strategies


def apply_filters(df, countries, crops, years, strategies):
    """
    Apply selected filters to the dataframe
    
    Args:
        df (DataFrame): Cleaned data to filter
        countries (list): Selected countries
        crops (list): Selected crop types
        years (tuple): Year range (min, max)
        strategies (list): Selected adaptation strategies
    
    Returns:
        DataFrame: Filtered dataframe
    """
    dff = df.copy()
    
    # Apply country filter
    if countries:
        dff = dff[dff["Country"].isin(countries)]
    
    # Apply crop filter
    if crops:
        dff = dff[dff["Crop_Type"].isin(crops)]
    
    # Apply year range filter
    year_min, year_max = years
    dff = dff[(dff["Year"] >= year_min) & (dff["Year"] <= year_max)]
    
    # Apply strategy filter
    if strategies:
        dff = dff[dff["Adaptation_Strategies"].isin(strategies)]
    
    return dff
