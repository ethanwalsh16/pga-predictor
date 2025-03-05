import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# ESPN leaderboard URLs
t_id = 401703489
URL = "https://www.espn.com/golf/leaderboard/_/tournamentId/" + str(t_id)

for i in range(0,9):
	# Send request to scrape data
	headers = {"User-Agent": "Mozilla/5.0"}
	response = requests.get(URL, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")

	# Find leaderboard table
	leaderboard = soup.find("table", class_="Table")

	# Extract headers
	headers = [th.text for th in leaderboard.find("thead").find_all("th")]

	# Extract player data
	data = []
	for row in leaderboard.find("tbody").find_all("tr"):
		cols = [td.text.strip() for td in row.find_all("td")]
		data.append(cols)

	# Convert to DataFrame
	df = pd.DataFrame(data, columns=headers)

	# Show first few rows
	print(df.head())

	# Save to CSV
	df.to_csv("golf_leaderboard" + str(i) + ".csv", index=False)

#Basic EDA: Distribution of player scores
df['SCORE'] = pd.to_numeric(df['SCORE'], errors='coerce')  # Ensure numeric scores
plt.hist(df['SCORE'].dropna(), bins=30, edgecolor='black')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Distribution of Tournament Scores')
plt.show()

# Save cleaned data
df.to_csv("golf_tournament_results.csv", index=False)
