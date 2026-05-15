"""It cleans each raw dataset and saves processed files in data/processed/
by standardizing county names, selecting needed columns, keeping usable rows,
and preparing the Zillow, ACS, and crime data for integration."""

import os            
import pandas as pd  

processed_data_folder="data/processed"            
os.makedirs(processed_data_folder, exist_ok=True) # Makes the data/raw folder if it doesn't already exist. exist_ok=True meaning if the folder already exist, don't give error, continue.

def clean_county_name(name):                      # Converts the county name to string, removes extra spaces, and removes the word "County".
    name=str(name).strip()
    name=name.replace(" County","")
    return name

def clean_zillow_data():                              
    input_path="data/raw/zillow_county_zhvi_raw.csv"  
    output_path="data/processed/zillow_clean.csv"     
    df=pd.read_csv(input_path)                        # Reads the raw Zillow csv file into a panda DataFrame.
    df["county_name"]=df["county_name"].apply(clean_county_name)      # Cleans the county names by removing extra words and spaces by using helper function. 
    df["state"]=df["state"].astype(str).str.strip()                   # Converts the state column to string type and remove extra spaces.
    df["zhvi"]=df["zhvi"].astype(str).str.replace(",","").str.strip() # Converts zhvi values to string, removes commas and extra spaces.
    df=df[df["state"]=="CA"]                # Keeps only rows where the state is Califonia.
    df=df[df["county_name"]!=""]            # Removes rows with missing or empty county names.
    df=df[df["zhvi"]!=""]                   # Removes rows with missing or empty zhvi values.
    df=df[["county_name","state","zhvi"]]   # Keeps only the needed columns for integration.
    df.to_csv(output_path,index=False)      # Saves the cleaned Zillow data as a csv file without the pandas index column.
    print(f"Saved cleaned Zillow data: {output_path}") 

def clean_acs_data():                                            # Cleans acs median household incme data for California counties.
    input_path="data/raw/acs_income_raw.csv"                     
    output_path="data/processed/acs_income_clean.csv"            
    df=pd.read_csv(input_path,dtype=str)                         # Reads the raw crime csv file and treats all columns as strings to avoid mixed data type warnnigs. 
    df=df.rename(columns={"B19013_001E": "median_income"})       # Renames the acs income column to simple name median_income.
    df["state"]=df["state"].astype(str).str.zfill(2)             # Convets the state columns to string and keeps the format of two digits.
    df["county_name"]=df["NAME"].str.replace(", California","",regex=False).str.strip()  # Cleans the county name by removng ",Californai" and extra spaces.
    df["county_name"]=df["county_name"].apply(clean_county_name) # Uses the helper function clean_county_name to standardize county names.
    df=df[df["state"]=="06"]                  # keeps only the code number 06 meaning California rows.
    df=df[df["county_name"]!=""]              # Removes rows with missing county names.
    df=df.dropna(subset=["median_income"])    # Removes rows with missing median income values.
    df=df[["county_name","median_income"]]    # Keeps only the needed columns for integration.
    df.to_csv(output_path,index=False)        # Saves the cleaned acs data as csv file.
    print(f"Saved cleaned ACS data: {output_path}")

def clean_crime_data():                                          # Cleans California violent crime data and keeps the latest year for each county.
    input_path="data/raw/ca_violent_crime_raw.csv"                      
    output_path="data/processed/crime_clean.csv"                 
    df=pd.read_csv(input_path,dtype=str)                         # Reads the raw crime csv file into panda DataFrame
    df=df[df["geotype"]=="CO"]                                   # Keeps only conty level crime records.
    df=df[df["strata_level_name"]=="Violent crime total"]        # Keeps only the total violent crime rate rows, not separate crime categories.
    df["county_name"]=df["county_name"].astype(str).str.strip()  # Cleasn county names using the helper function.
    df["county_name"]=df["county_name"].apply(clean_county_name) # Standardizes county names by using helper function clean_county_name. 
    df["rate"]=df["rate"].astype(str).str.strip()                # Removes extra spaces from the crime rate column.
    df["reportyear"]=df["reportyear"].astype(str).str.strip()    # Converts report years to text and removes extra spaces.
    df=df[df["reportyear"]!=""]                                  # Removes rows with empty report year values if the reportyear column is still text.
    df=df[df["county_name"]!=""]                                 # Removes rows with empty county names.
    df=df[df["rate"]!=""]                                        # Removes rows with empty crime rate values.
    df["reportyear"]=pd.to_numeric(df["reportyear"],errors="coerce") # Converts report years to numbers and changes invalid values to missing.
    df=df.dropna(subset=["reportyear"])                          # Removes rows where report year could not be converted.
    df["reportyear"]=df["reportyear"].astype(int)                # Converts report years to integers so the latest year can be selected. 
    df=df.sort_values("reportyear")                              # Sorts the data so the latest year appears last for each county.
    df=df.drop_duplicates(subset="county_name",keep="last")      # Keeps only the latest row for each county.
    df=df.rename(columns={"rate":"violent_crime_rate"})          # Renames the crime rate column to a clearer name.
    df=df[["county_name","violent_crime_rate","reportyear"]]     # Keeps only the columns needed for integration.
    df.to_csv(output_path,index=False)                           # Saves the cleaned crime data as csv file.
    print(f"Saved cleaned crime data: {output_path}")            

def main():
    clean_zillow_data()
    clean_acs_data()
    clean_crime_data()
    print("All cleaned files saved successfully.")

if __name__ == "__main__":
    main()       