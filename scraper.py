import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Function to scrape leaderboard data
def scrape_leaderboard(t_id):
    
    URL = f"https://www.espn.com/golf/leaderboard/_/tournamentId/{t_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Ensuring correct table is selected
    tables = soup.find_all("table", class_="Table")

    if len(tables) > 1:
        leaderboard = tables[1]
    else:
        leaderboard = tables[0]

    # Extract headers
    headers = [th.text for th in leaderboard.find("thead").find_all("th")]

    # Extract player data
    data = []
    for row in leaderboard.find("tbody").find_all("tr"):
        cols = [td.text.strip() for td in row.find_all("td")]
        data.append(cols)

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

# Initialize data structure
players_data = {}

# List of tournament IDs
tournament_ids = [401703489, 401703490, 401703492, 401703493, 401703494, 401703495, 401703496, 401703497] 

for t_id in tournament_ids:
	df = scrape_leaderboard(t_id)

	# Process each player's data
	for _, row in df.iterrows():
		name = row['PLAYER']
		if('(a)' in name):
			continue
		score = pd.to_numeric(row['SCORE'], errors='coerce')
		winnings = pd.to_numeric(row['EARNINGS'].replace('$', '').replace(',', ''), errors='coerce')

		if name not in players_data:
			players_data[name] = {'total_score': 0, 'total_winnings': 0, 'tournaments_played': 0, 'average_score': 0, 'average_winnings': 0, 'prediction': 0}

		players_data[name]['total_score'] += score
		players_data[name]['total_winnings'] += winnings
		players_data[name]['tournaments_played'] += 1
    
for player in players_data:
	players_data[player]['average_score'] = players_data[player]['total_score'] / players_data[player]['tournaments_played']
	players_data[player]['prediction'] += players_data[player]['total_score']*(-0.1)
	players_data[player]['prediction'] += players_data[player]['average_score']*(-1.5)
	players_data[player]['average_winnings'] = players_data[player]['total_winnings'] / players_data[player]['tournaments_played']

# Convert players_data to DataFrame
players_df = pd.DataFrame.from_dict(players_data, orient='index')
players_df.reset_index(inplace=True)
players_df.rename(columns={'index': 'player'}, inplace=True)

# Printing relevant results

players_df = players_df.sort_values(by='average_score', ascending=True)
print("Top 5 players by average score (2025):")
print("\n")
print(players_df.head())
print("\n")

players_df = players_df.sort_values(by='total_score', ascending=True)
print("Top 5 players by total score (2025):")
print("\n")
print(players_df.head())
print("\n")

print("\nNow including 2024 Arnold Palmer Invitational")

df = scrape_leaderboard(401580338)
# Process each player's data
for _, row in df.iterrows():
	name = row['PLAYER']
	if('(a)' in name):
		continue
	score = pd.to_numeric(row['SCORE'], errors='coerce')
	winnings = pd.to_numeric(row['EARNINGS'].replace('$', '').replace(',', ''), errors='coerce')

	if name not in players_data and '(a)' not in name:
		players_data[name] = {'total_score': 0, 'total_winnings': 0, 'tournaments_played': 0, 'average_score': 0, 'average_winnings': 0, 'prediction': 0}

	players_data[name]['total_score'] += score
	players_data[name]['total_winnings'] += winnings
	players_data[name]['tournaments_played'] += 1
	players_data[name]['prediction'] += score*(-0.8)

sg_list = ["Rory McIlroy","Taylor Pendrith","Keitch Mitchell","Kurt Kitayama"]
    
for player in players_data:
	players_data[player]['average_score'] = players_data[player]['total_score'] / players_data[player]['tournaments_played']
	players_data[player]['average_winnings'] = players_data[player]['total_winnings'] / players_data[player]['tournaments_played']
	if players_data[player] in sg_list:
		print("Yep")
		players_data[player]['prediction'] *= 99

# Convert players_data to DataFrame
players_df = pd.DataFrame.from_dict(players_data, orient='index')
players_df.reset_index(inplace=True)
players_df.rename(columns={'index': 'player'}, inplace=True)
players_df = players_df[players_df['tournaments_played'] > 2]

# Printing relevant results

players_df = players_df.sort_values(by='average_score', ascending=True)
print("Top 5 players by average score (incl 2024 AP inv):")
print("\n")
print(players_df.head())
print("\n")

players_df = players_df.sort_values(by='total_score', ascending=True)
print("Top 5 players by total score (incl 2024 AP inv):")
print("\n")
print(players_df.head())
print("\n")

players_df = players_df.sort_values(by='prediction', ascending=False)
print("Top 5 players by prediction:")
print("\n")
print(players_df.head())
print("\n")

