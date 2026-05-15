"""It integrates the cleaned datasets into one county level file by joining 
Zillow housing values, ACS median household income, and California violent 
crime data using county_name and saving the final integrated_county_data.csv file."""

import pandas as pd         

def main():
    zillow_df=pd.read_csv("data/processed/zillow_clean.csv")          # Reads the cleaned Zillow housing value data.
    acs_df=pd.read_csv("data/processed/acs_income_clean.csv")         # Reads the cleaned ACS median household income data.
    crime_df=pd.read_csv("data/processed/crime_clean.csv")            # Reads the cleaned California violent crime data.
    merged_df=zillow_df.merge(acs_df,on="county_name",how="outer")    # Merges Zillow and ACS data by county_name and keeps all counties even if a county appears in only one file.
    merged_df=merged_df.merge(crime_df,on="county_name",how="outer")  # Adds criem data to the previous merged dataset by county_name and keeps all counties from both datasets.
    merged_df=merged_df[["county_name","zhvi","median_income","violent_crime_rate","reportyear"]] # Keeps only the needed final columns.
    output_path="data/processed/integrated_county_data.csv"           # Sets the output path for the integrated dataset.
    merged_df.to_csv(output_path,index=False)                         # Saves the merged DataFrame as a csv file without the pandas index.
    print(f"Saved integrated file: {output_path}")

if __name__ == "__main__":
    main()      
