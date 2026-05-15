"""It analyzes the integrated county-level dataset and creates visualizations
by computing summary results and producing plots that compare housing values,
income, and violent crime across California counties, then saving outputs in results/."""

import os                          
import pandas as pd                
import matplotlib.pyplot as plt    
import seaborn as sns              

def load_integrated_data():          # Loads the final merged dataset.
    input_path="data/processed/integrated_county_data.csv"  
    df=pd.read_csv(input_path)       # Reads the integrated csv file into a DataFrame.
    return df                        # Returns the DataFrame for analysis and visualization.

def clean_numeric_columns(df):       # Converts important columns to numeric values.
    df["zhvi"]=pd.to_numeric(df["zhvi"],errors="coerce")  # Converts housing value to numeric.
    df["median_income"]=pd.to_numeric(df["median_income"],errors="coerce")  # Converts income to numeric.
    df["violent_crime_rate"]=pd.to_numeric(df["violent_crime_rate"],errors="coerce")  # Converts crime rate to numeric.
    df=df.dropna(subset=["zhvi","median_income","violent_crime_rate"])  # Removes rows with missing needed values and returns the cleaned DataFrame.
    return df                        

def save_summary_results(df):        # Saves summary statistics for the final dataset.
    output_path="results/summary_results.csv"  
    summary=df[["zhvi","median_income","violent_crime_rate"]].describe()  # Calculates summary statistics.
    summary.to_csv(output_path)      # Saves the summray statistics as a csv file.

def plot_income_vs_housing(df):      # Creates a scatter plot comparing income and housing value.
    plt.figure(figsize=(10,6))       
    sns.scatterplot(data=df,x="median_income",y="zhvi")  
    plt.title("Median Income vs. Zillow Home Value Index")  
    plt.xlabel("Median Household Income")      
    plt.ylabel("Zillow Home Value Index")      
    plt.tight_layout()                         # Adjusts layout spacing.
    plt.savefig("results/income_vs_housing.png")  
    plt.close()                                

def plot_crime_vs_housing(df):       # Creates a scatter plot comparing crime rate and housing value.
    plt.figure(figsize=(10,6))       
    sns.scatterplot(data=df,x="violent_crime_rate",y="zhvi")  
    plt.title("Violent Crime Rate vs. Zillow Home Value Index") 
    plt.xlabel("Violent Crime Rate") 
    plt.ylabel("Zillow Home Value Index")        
    plt.tight_layout()              
    plt.savefig("results/crime_vs_housing.png")  
    plt.close()                                

def plot_top_housing_counties(df):   # Creates a bar chart for counties with the highest housing values.
    top_df=df.sort_values("zhvi",ascending=False).head(10)  # Selects the top 10 counties by housing value.
    plt.figure(figsize=(10,6))   
    plt.barh(top_df["county_name"],top_df["zhvi"])   
    plt.gca().invert_yaxis() 
    plt.title("Top 10 California Counties by Zillow Home Value Index")  
    plt.xlabel("Zillow Home Value Index")      
    plt.ylabel("County")            
    plt.tight_layout()              
    plt.savefig("results/top_10_housing_counties.png") 
    plt.close()                                

def plot_top_crime_counties(df):     # Creates a bar chart for counties with the highest violent crime rates.
    top_df=df.sort_values("violent_crime_rate",ascending=False).head(10)  # Selects the top 10 counties by crime rate.
    plt.figure(figsize=(10,6))      
    plt.barh(top_df["county_name"],top_df["violent_crime_rate"])
    plt.gca().invert_yaxis()
    plt.title("Top 10 California Counties by Violent Crime Rate")  
    plt.xlabel("Violent Crime Rate") 
    plt.ylabel("County")            
    plt.tight_layout()               
    plt.savefig("results/top_10_crime_counties.png")  
    plt.close()                               

def plot_correlation_heatmap(df):    # Creates a heatmap showing relationships between numeric variables.
    corr=df[["zhvi","median_income","violent_crime_rate"]].corr()  # Calculates correlations.
    plt.figure(figsize=(8,6))       
    sns.heatmap(corr,annot=True,cmap="Blues")  # Creates the heatmap with correlation values.
    plt.title("Correlation Between Housing Value, Income, and Crime") 
    plt.tight_layout()              
    plt.savefig("results/correlation_heatmap.png")  
    plt.close()                               

def main():                         
    os.makedirs("results",exist_ok=True)    
    df=load_integrated_data()        
    df=clean_numeric_columns(df)     
    save_summary_results(df)         
    plot_income_vs_housing(df)       
    plot_crime_vs_housing(df)        
    plot_top_housing_counties(df)    
    plot_top_crime_counties(df)      
    plot_correlation_heatmap(df)    

if __name__=="__main__":             
    main()                          