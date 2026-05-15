"""It scrapes Zillow housing data links and extracts California county housing values
by finding the Zillow dataset link, then downloading the Zillow CSV, extracting California
county rows, and helping  get_data.py file to save zillow_county_zhvi_raw.csv, 
and zillow_full_download.csv."""

import requests               
from bs4 import BeautifulSoup 
import argparse               
import pandas as pd           

def find_zillow_dataset():    # Finds and returns the first usable Zillow county level dataset.
    zillow_page="https://www.zillow.com/research/data/"   
    response=requests.get(zillow_page)                    # Sends request to Zillow research data page.
    soup=BeautifulSoup(response.text,"html.parser")       # Parses the HTML page so Python can search inside it.
    links=soup.find_all("a")                              # Finds all link tags on the webpage.
    for link in links:                                    # Loops through each link found on the page and gets the actual URL from the link.
        href=link.get("href")                             
        if href is not None and "County_zhvi" in href and href.endswith(".csv"): # Checks if the link is a county ZHVI CSV file, and returns the first matching Zillow county CSV link.
            return href                                   
    zillow_url="https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv" # Backup Zillow county ZHVI CSV link.
    return zillow_url                                     # Returns the backup Zillow CSV link if BeautifulSoup does not find one.

def extract_california_latest(df):  # Extracts California counties and the latest Zillow housing value.
    if len(df)==0:                  # Checks whether the Zillow DataFrame has no rows.
        print("No Zillow rows were found.")
        return pd.DataFrame() 
    if "State" in df.columns:       # Checks if the state colunm is named State.
        state_col="State"           # Uses State as the state column.
    else:
        state_col="StateName"       # Uses StateName if State does not exist.
    california_df=df[df[state_col].astype(str).str.upper()=="CA"].copy()  # Keeps only rowss where the state is Californai.
    if len(california_df)==0:       # Checks if no California rows could found.
        print("No California rows were found in the Zillow dataset.")
        return pd.DataFrame()
    date_columns=california_df.columns[california_df.columns.str.match(r"\d{4}-\d{2}-\d{2}")]   # Finds date columns using regular expression.
    latest_col=date_columns[-1]     # Selects the most recent Zillow date column the last one.
    result_df=california_df[["RegionName",state_col,latest_col]].copy()                         # Keeps only needed colunms.
    result_df=result_df.rename(columns={"RegionName":"county_name",state_col:"state",latest_col:"zhvi"})              # Renames columns to match the rest of the project.
    result_df["county_name"]=result_df["county_name"].astype(str).str.replace(" County","", regex=False).str.strip()  # Removes the word County and extra spaces from county names.
    result_df=result_df.sort_values("county_name")      # Sorts counties alphabetically.
    return result_df                # Returns the cleaned California Zillow DataFrame.

def print_rows(df):                 # Prints the DataFrame rows as csv text.
    if len(df)==0:                  # Checks if there are no rows to print.
        return
    print(df.to_csv(index=False))   # Prints the DataFrame as csv text.

def write_csv(df,path):              # Saves a DataFrame as a csv file.
    df.to_csv(path,index=False)      # Saves the DataFrame without pandas index column.

def main():                         # Runs the full scraping and extraction process.
    parser=argparse.ArgumentParser(description="Scrape California counties Zillow housing data")  # Creates the command line parser.
    parser.add_argument("--scrape",type=int,help="Print only the first N rows")  # Adds an option to print only the first N rows.
    parser.add_argument("--save",type=str,help="Save the complete dataset to a csv file")  # Adds an option to save the final data to a csv file.
    args=parser.parse_args()                    # Reads the command line arguments.
    zillow_url=find_zillow_dataset()            # Gets the Zillow dataset URL.
    response=requests.get(zillow_url)           # Downloads the Zillow CSV file using requests.
    response.raise_for_status()                 # Stops the program if the Zillow request fails.
    with open("data/raw/zillow_full_download.csv","wb") as f: # Opens a raw CSV file in write mode and writes the downloaded Zillow CSV content into the file.
        f.write(response.content)                              
    raw_df=pd.read_csv("data/raw/zillow_full_download.csv")    # Reads the saved Zillow CSV file into a pandas DataFrame.
    final_df=extract_california_latest(raw_df)                 # Extracts California county rows and latest ZHVI values.
    if args.save:                               # Checks if the user gave a save path.
        final_df.to_csv(args.save,index=False)  # If yes, saves the final Zillow data to a csv file.
    if args.scrape is not None:                 # Checks if the user requested only the first N rows.
        print_rows(final_df.head(args.scrape))  # If yes, prints only the first N rows.
    else:
        print_rows(final_df)                    # If not, prints all rows.

if __name__ == "__main__":          
    main()                          