import requests
import pandas as pd
import matplotlib.pyplot as plt

# DataGolf API endpoint for tournament results
API_URL = "https://feeds.datagolf.com/historical-tournament-results"
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

# Fetch tournament results (example: last 5 years, PGA Tour)
params = {
    "tour": "pga",
    "years": "2019-2023",
    "key": API_KEY
}
response = requests.get(API_URL, params=params)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)
print(df.head())  # Check the first few rows

# Basic EDA: Distribution of player scores
df['score'] = pd.to_numeric(df['score'], errors='coerce')  # Ensure numeric scores
plt.hist(df['score'].dropna(), bins=30, edgecolor='black')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Distribution of Tournament Scores')
plt.show()

# Save cleaned data
df.to_csv("golf_tournament_results.csv", index=False)
