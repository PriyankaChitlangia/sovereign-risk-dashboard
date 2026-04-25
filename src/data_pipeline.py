import pandas as pd
import numpy as np
import os
import glob

# Constants
WEO_FILE = "weoapr2025all.xls"
FSI_PATTERN = "dataset_*_DEFAULT_INTEGRATION_IMF.STA_FSIC*.csv"
MONA_FILE = "DownloadData.xlsx"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "processed_data.csv")
YEARS_OF_INTEREST = [str(y) for y in range(2001, 2029)]

# WEO Subject Codes of interest
# NGDP_RPCH: Gross domestic product, constant prices (Percent change)
# PCPIPCH: Inflation, average consumer prices (Percent change)
# GGXWDG_NGDP: General government gross debt (Percent of GDP)
# BCA_NGDPD: Current account balance (Percent of GDP)
WEO_INDICATORS = {
    'NGDP_RPCH': 'GDP_Growth',
    'PCPIPCH': 'Inflation',
    'GGXWDG_NGDP': 'Gov_Debt_GDP',
    'BCA_NGDPD': 'Current_Account_Balance'
}

def load_and_clean_weo(filepath):
    print("Loading WEO Data...")
    df = pd.read_csv(filepath, sep='\t', encoding='utf-16-le', na_values=['n/a', '--'])
    
    # Filter for interesting indicators
    df = df[df['WEO Subject Code'].isin(WEO_INDICATORS.keys())]
    
    # Melt years into long format
    id_vars = ['WEO Country Code', 'ISO', 'Country', 'WEO Subject Code', 'Subject Descriptor']
    df_melt = df.melt(id_vars=id_vars, value_vars=YEARS_OF_INTEREST, 
                      var_name='Year', value_name='Value')
    
    # Clean values
    df_melt['Value'] = df_melt['Value'].replace({',': ''}, regex=True).astype(float)
    df_melt['Year'] = df_melt['Year'].astype(int)
    
    # Pivot to make indicators columns
    df_pivot = df_melt.pivot_table(index=['ISO', 'Country', 'Year'], 
                                   columns='WEO Subject Code', 
                                   values='Value').reset_index()
    
    # Rename columns
    df_pivot = df_pivot.rename(columns=WEO_INDICATORS)
    return df_pivot

def load_and_clean_fsi(filepath):
    print("Loading FSI Data...")
    df = pd.read_csv(filepath, encoding='latin1', low_memory=False)
    
    # FSI data is wide format: COUNTRY, INDICATOR, and then years
    # Filter for the years we care about
    year_cols = [str(y) for y in range(2001, 2029)]
    
    # Check if we have the year columns in this dataframe
    actual_years = [y for y in year_cols if y in df.columns]
    
    # We will use 'COUNTRY' as our country identifier. In IMF data, 'COUNTRY' often holds ISO-like codes or names.
    id_vars = ['COUNTRY', 'INDICATOR']
    if 'SERIES_NAME' in df.columns:
        id_vars.append('SERIES_NAME')
        
    df_melt = df.melt(id_vars=id_vars, value_vars=actual_years, 
                      var_name='Year', value_name='Value')
                      
    df_melt['Year'] = df_melt['Year'].astype(int)
    
    # FSI_Indicator will be the INDICATOR column
    df_melt = df_melt.rename(columns={'COUNTRY': 'Country', 'INDICATOR': 'FSI_Indicator'})
    
    # Remove rows with NaN values
    df_melt = df_melt.dropna(subset=['Value'])
    
    df_pivot = df_melt.pivot_table(index=['Country', 'Year'], columns='FSI_Indicator', values='Value').reset_index()
    
    # Find most common indicators
    counts = df_pivot.count()
    top_cols = counts.drop(['Country', 'Year']).nlargest(5).index.tolist()
    print("Top FSI indicators found:", top_cols)
    
    df_pivot = df_pivot[['Country', 'Year'] + top_cols]
    
    return df_pivot

def load_and_clean_mona(filepath):
    print("Loading MONA Data...")
    df = pd.read_excel(filepath)
    
    df['ApprovalDate'] = pd.to_datetime(df['ApprovalDate'], errors='coerce')
    df['ApprovalYear'] = df['ApprovalDate'].dt.year
    
    # We only care about country and year of approval
    # 'CountryName' might need mapping to ISO. Let's return just Country and Year.
    crisis_events = df[['CountryName', 'ApprovalYear']].dropna().drop_duplicates()
    return crisis_events

def create_labels(df_merged, crisis_events):
    print("Creating Labels...")
    # Initialize label
    df_merged['Crisis_Next_3_Years'] = 0
    
    countries_mona = crisis_events['CountryName'].unique()
    countries_weo = df_merged['Country'].dropna().unique()
    
    from difflib import get_close_matches
    mapping = {}
    for c in countries_mona:
        # MONA names are often all caps like "AFGHANISTAN,ISLAMIC REPUBLIC OF"
        c_clean = c.split(',')[0].title()
        
        # Try direct match first
        if c_clean in countries_weo:
            mapping[c] = c_clean
            continue
            
        matches = get_close_matches(c_clean, countries_weo, n=1, cutoff=0.75)
        if matches:
            mapping[c] = matches[0]
        else:
            # lower cutoff as fallback
            matches = get_close_matches(c_clean, countries_weo, n=1, cutoff=0.6)
            if matches:
                mapping[c] = matches[0]
            
    crisis_events['Country_WEO'] = crisis_events['CountryName'].map(mapping)
    
    matched_count = crisis_events['Country_WEO'].notna().sum()
    print(f"Matched {matched_count} out of {len(crisis_events)} crisis events to WEO countries.")
    
    crisis_events = crisis_events.dropna(subset=['Country_WEO'])
    
    # Create the label
    label_count = 0
    for _, row in crisis_events.iterrows():
        country = row['Country_WEO']
        year = row['ApprovalYear']
        
        # If crisis in Year T, then T-1, T-2, T-3 get Label = 1
        mask = (df_merged['Country'] == country) & (df_merged['Year'].isin([year-1, year-2, year-3]))
        if mask.any():
            df_merged.loc[mask, 'Crisis_Next_3_Years'] = 1
            label_count += mask.sum()
            
    print(f"Total positive labels created: {label_count}")
    return df_merged

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # 1. WEO Data
    df_weo = load_and_clean_weo(WEO_FILE)
    
    # 2. FSI Data
    fsi_files = glob.glob(FSI_PATTERN)
    if not fsi_files:
        raise FileNotFoundError(f"No FSI file matching {FSI_PATTERN} found.")
    df_fsi = load_and_clean_fsi(fsi_files[0])
    
    # 3. Merge WEO and FSI
    # WEO has 'Country' and FSI has 'Country'
    df_merged = pd.merge(df_weo, df_fsi, on=['Country', 'Year'], how='left')
    
    # 4. MONA Data & Labels
    crisis_events = load_and_clean_mona(MONA_FILE)
    df_final = create_labels(df_merged, crisis_events)
    
    # 5. Save
    print(f"Saving processed data to {OUTPUT_FILE}...")
    df_final.to_csv(OUTPUT_FILE, index=False)
    print("Done! Data shape:", df_final.shape)

if __name__ == "__main__":
    main()
