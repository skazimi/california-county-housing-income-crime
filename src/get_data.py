"""It downloads all project data into data/raw/ by collecting Zillow 
housing data, American Community Survey (ACS) median household income data, and California violent 
crime data, then saving the raw files for later cleaning."""

import os           
import json         
import requests     
import pandas as pd 
from scraper import extract_california_latest, find_zillow_dataset, write_csv

raw_data_folder="data/raw"  # The original raw data files before cleaning stores in this folder.
os.makedirs(raw_data_folder,exist_ok=True)  # Makes the data/raw folder if it doesn't already exist. exist_ok=True meaning if the folder already exist, don't give error, continue.

ACS_API_KEY=os.getenv("ACS_API_KEY")  # Gets the ACS API key from the environment variable, and keeps it out of the code file for privacy.
ACS_URL=("https://api.census.gov/data/2024/acs/acs5" # Downloads 2024 county level median household income data.
           "?get=NAME,B19013_001E"  # get=NAME (county name), B19013_001E (median household income estimate)
           "&for=county:*"          # for=county:* (requests all counties)
           "&in=state:06")          # instate:06= (requests only California)         
if ACS_API_KEY:
    ACS_URL=ACS_URL+f"&key={ACS_API_KEY}"  # The API key adds only if it exists in the computer.
headers={"User-Agent":"Mozilla/5.0"}       

def save_zillow_data(): 
    zillow_url=find_zillow_dataset()                                  
    response=requests.get(zillow_url,headers=headers)                 # Downloads the Zillow CSV file using requests and stops the program if the Zillow request fails.
    response.raise_for_status()                                       
    with open("data/raw/zillow_full_download.csv","wb") as f:         # Opens a raw CSV file in write mode and writes the downloaded Zillow CSV content into the file..
        f.write(response.content)                                     
    zillow_rows=pd.read_csv("data/raw/zillow_full_download.csv")      # Reads the saved Zillow CSV file into a pandas DataFrame.
    california_zillow_rows=extract_california_latest(zillow_rows)     # Filters only the latest California county level Zillow data.
    write_csv(california_zillow_rows,"data/raw/zillow_county_zhvi_raw.csv") # Saves the filtered California Zillow data.
    print("Saved Zillow raw data: data/raw/zillow_county_zhvi_raw.csv")

def save_acs_data():                              
    response=requests.get(ACS_URL,headers=headers) # Sends a request to the ACS Census API and stops the program and shows an error if the request failes.
    response.raise_for_status()                    
    print("ACS request was successful")  
    rows=response.json()
    with open("data/raw/acs_income_raw.json","w",encoding="utf-8") as f: # Saves the original ACS response as a raw json file
        json.dump(rows,f,indent=2) 
    df=pd.DataFrame(rows[1:],columns=rows[0])            # rows[:1] is the actual data, and rows[0] is the header row
    df.to_csv("data/raw/acs_income_raw.csv",index=False) # Saves the DataFrame as a csv file without adding extra index column.
    print("Saved ACS raw data: data/raw/acs_income_raw.csv")

def save_crime_data(): 
    csv_link="https://data.ca.gov/datastore/dump/358f23e6-f0f9-45e1-864c-fbad0f0b84b3?bom=True" 
    response=requests.get(csv_link,headers=headers)  # Sends a request to download the crime csv file and stops the program if the request fails.
    response.raise_for_status()                      
    with open("data/raw/ca_violent_crime_raw.csv","wb") as f:  # Opens a raw csv file in write mode and writes the downloaded csv contnet into the file.
        f.write(response.content)                    
    print("Saved crime raw data: data/raw/ca_violent_crime_raw.csv")

def main():
    save_zillow_data()                         
    save_acs_data()                                  
    save_crime_data()                                
    print("Raw data download step finished.")

if __name__ == "__main__":
    main()       