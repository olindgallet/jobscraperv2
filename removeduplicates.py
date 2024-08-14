import pandas as pd

# Load the CSV file
file_path = '/Users/lukegeel/Desktop/LinkedIn/AI Jobscraper/june2024/real estate/finalfinal.csv' 
df = pd.read_csv(file_path)

# Remove leading and trailing whitespace from 'Company' and 'Title' columns
df['Company'] = df['Company'].str.strip()
df['Title'] = df['Title'].str.strip()
df['Link'] = df['Link'].str.strip()
df['Location'] = df['Location'].str.strip()

# Remove duplicate rows based on 'Company' and 'Title', keeping the first occurrence
df_deduplicated = df.drop_duplicates(subset=['Company', 'Title', 'Link', 'Location'], keep='first')

# Save the deduplicated dataframe to a new CSV file
df_deduplicated.to_csv('/Users/lukegeel/Desktop/LinkedIn/AI Jobscraper/june2024/real estate/finalfinal2.csv' , index=False)

print("Duplicates removed")