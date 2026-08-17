import requests 
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


FPL_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

response  = requests.get(FPL_URL)

data = response.json()
#print(type(data))
#print(data.keys())

players = data["elements"]
#print(players[0])

#print(len(players))

'''first_player = players[0]
print(first_player["web_name"])
print(first_player["total_points"])'''

midfielders = []

for player in players :
    if player["element_type"] == 3:
        midfielders.append(player)

#print(len(midfielders))
'''for player in midfielders[:5] : 
    print(player["web_name"])'''

midfielders_sorted = sorted(midfielders, key = lambda player : player["total_points"], reverse = True)
top_5_midfielders = midfielders_sorted[:5]

'''for player in top_5_midfielders: 
    print(player["web_name"], player["total_points"])'''

top_5_data = []

for player in top_5_midfielders:
    top_5_data.append({
        "name": player["web_name"],
        "points": player["total_points"],
        "price": player["now_cost"] / 10,
        "goals": player["goals_scored"],
        "assists": player["assists"],
        "minutes": player["minutes"]
    })

'''for player in top_5_data:
    print(player)'''

prompt = f"""
Here is the current FPL data for the top scoring midfielders:

{top_5_data}

Based only on this data, tell me who the top 5 scoring
midfielders are. Give me their names and total points.
"""


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print(response.text)