import os
import requests
import pandas as pd
from sqlalchemy import create_engine

# Database connection URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@database:5432/interview_prep")

# Define the table name
TABLE_NAME = "question"

# Base URL of the GitHub repository
BASE_URL = "https://raw.githubusercontent.com/krishnadey30/LeetCode-Questions-CompanyWise/master/"

# Fetch the list of available CSV files from the repository
def fetch_csv_file_list():
    repo_api_url = "https://api.github.com/repos/krishnadey30/LeetCode-Questions-CompanyWise/contents"
    response = requests.get(repo_api_url)
    if response.status_code == 200:
        files = response.json()
        csv_files = [file['name'] for file in files if file['name'].endswith('.csv')]
        return csv_files
    else:
        print("Failed to fetch file list from GitHub.")
        return []

# Extract unique company names from the list of CSV files
def get_unique_company_names(csv_files):
    unique_companies = set()
    for file_name in csv_files:
        if "_6months.csv" in file_name or "_1year.csv" in file_name or "_2year.csv" in file_name or "_alltime.csv" in file_name:
            company_name = file_name.split('_')[0]
            unique_companies.add(company_name)
    return list(set(unique_companies))

# Get the best available CSV file for a given company
def get_best_available_csv(company, csv_files):
    preferred_order = ["6months", "1year", "2year", "alltime"]
    for time_period in preferred_order:
        file_name = f"{company}_{time_period}.csv"
        if file_name in csv_files:
            return file_name
    return None

# Fetch data from a CSV file and insert it into the database
def fetch_and_store_data(file_name, engine):
    file_url = f"{BASE_URL}{file_name}"
    try:
        df = pd.read_csv(file_url)
        df = df.rename(columns={
            'Title': 'question',
            'Acceptance': 'acceptance',
            'Difficulty': 'difficulty',
            'Leetcode Question Link': 'question_link'
        })
        df['company'] = file_name.split('_')[0]
        df = df[['company', 'question', 'acceptance', 'difficulty', 'question_link']]
        df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)
        print(f"Data from {file_name} inserted successfully.")
    except Exception as e:
        print(f"Failed to process {file_url}: {e}")

# Main function to run the update process
def update_database():
    engine = create_engine(DATABASE_URL)
    csv_files = fetch_csv_file_list()
    company_names = get_unique_company_names(csv_files)

    for company in company_names:
        best_file = get_best_available_csv(company, csv_files)
        if best_file:
            fetch_and_store_data(best_file, engine)
        else:
            print(f"No CSV file found for {company}")

if __name__ == '__main__':
    update_database()
