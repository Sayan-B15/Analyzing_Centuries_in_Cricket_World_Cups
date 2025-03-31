import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config to change the app title and logo
st.set_page_config(page_title="Cricket World Cup Centuries Analysis", page_icon="🏏")

# Custom CSS
st.markdown(
    """
    <style>
    /* Custom page styling */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
    }

    /* Title styling */
    .css-1xarl3l h1 {
        color: #f0a500;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
    }

    /* Subtitle styling */
    .css-16huue1 h2 {
        color: #ff6347;
        font-size: 2rem;
        font-weight: bold;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid #333;
        background-color: #1e1e1e;
        color: #e0e0e0;
    }

    

    /* Plot styling */
    .stPlotlyChart {
        border: 2px solid #333;
        border-radius: 10px;
    }
    
    /* Adjusting plot size */
    .stPlot {
        max-width: 80%;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and Header
st.title("🏆 Cricket World Cup Centuries Analysis")

# Load the dataset
data = pd.read_csv('Cleaned-All-Cricket-World-Cup-Centuries.csv')

st.write("## 📊 Dataset Overview")
st.dataframe(data)

# Comparison of Centuries Scored by Teams against Different Oppositions
st.write("### ⚔️ Comparison of Centuries Scored by Teams against Different Oppositions")

# Group the data by Team and Opposition, then count the number of centuries
team_opposition_centuries = data.groupby(['Team', 'Opposition']).size().reset_index(name='Centuries')

# HTML styling for the centered table with improved contrast
def generate_centered_table_comparison(data):
    html = '<table style="width:100%; border-collapse: collapse; text-align: center; font-family: Arial, sans-serif;">'
    html += '<tr><th style="border: 1px solid #ddd; padding: 10px; background-color: #333; color: #fff;">Team</th><th style="border: 1px solid #ddd; padding: 10px; background-color: #333; color: #fff;">Opposition</th><th style="border: 1px solid #ddd; padding: 10px; background-color: #333; color: #fff;">Centuries</th></tr>'
    for _, row in data.iterrows():
        html += f'<tr><td style="border: 1px solid #ddd; padding: 8px; background-color: #f5f5f5; color: #333;">{row["Team"]}</td>'
        html += f'<td style="border: 1px solid #ddd; padding: 8px; background-color: #f5f5f5; color: #333;">{row["Opposition"]}</td>'
        html += f'<td style="border: 1px solid #ddd; padding: 8px; background-color: #f5f5f5; color: #333;">{row["Centuries"]}</td></tr>'
    html += '</table>'
    return html

# Generate and display the table with centered content for "Comparison of Centuries Scored"
st.markdown(generate_centered_table_comparison(team_opposition_centuries), unsafe_allow_html=True)


# Team performance at Old Trafford Cricket Ground, Manchester
selected_venue = 'Old Trafford Cricket Ground, Manchester'
st.write(f"### 🏟️ Team Performance in {selected_venue}")
team_venue_centuries = data.groupby(['Team', 'Venue']).size().reset_index(name='Centuries')
venue_data = team_venue_centuries[team_venue_centuries['Venue'] == selected_venue]
venue_data_sorted = venue_data.sort_values('Centuries', ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(venue_data_sorted['Team'], venue_data_sorted['Centuries'], color='#1f77b4')
plt.xlabel('Team', fontsize=12)
plt.ylabel('Number of Centuries', fontsize=12)
plt.title('Team Performance in ' + selected_venue, fontsize=14)
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
st.pyplot(plt)

# Top 5 Players with the Highest Number of Centuries
st.write("### 🏅 Top 5 Players with the Highest Number of Centuries")
def clean_runs_column(runs_value):
    if isinstance(runs_value, str):
        return int(runs_value.replace('*', ''))
    return runs_value

data['Runs'] = data['Runs'].apply(clean_runs_column)
player_centuries = data[data['Runs'] >= 100].groupby('Player').size().reset_index(name='Centuries')
player_centuries_sorted = player_centuries.sort_values('Centuries', ascending=False)
top_5_players = player_centuries_sorted.head(5)

colors = ['#FFB6C1', '#FFDAB9', '#90EE90', '#E6E6FA', '#ADD8E6']
sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_players, x='Player', y='Centuries', palette=colors, hue='Player', dodge=False, legend=False)
plt.xlabel('Player', fontsize=12)
plt.ylabel('Number of Centuries', fontsize=12)
plt.title('Top 5 Players with the Highest Number of Centuries', fontsize=14)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
st.pyplot(plt)

# Impact of Centuries on Match Results
st.write("### 🏆 Impact of Centuries on Match Results")
data['Match_Result'] = data['Result'].apply(lambda x: 'Won' if 'won' in x.lower() else 'Lost')
centuries_win_loss = data.groupby('Match_Result')['Player'].count()

plt.figure(figsize=(8, 6))
plt.bar(centuries_win_loss.index, centuries_win_loss.values, color=['#FF6347', '#4682B4'])
plt.xlabel('Match Result', fontsize=12)
plt.ylabel('Number of Centuries', fontsize=12)
plt.title('Impact of Centuries on Match Results', fontsize=14)
plt.tight_layout()
st.pyplot(plt)

# Players with Most 4s and 6s in Their Centuries
st.write("### 💥 Players with Most 4s and 6s in Their Centuries")
player_shots = data.groupby('Player')[['4s', '6s']].sum()

# Players with Most 4s
st.write("#### 🔥 Players with the Most 4s")
players_most_4s = player_shots['4s'].sort_values(ascending=False).head(10)

# Players with Most 6s
st.write("#### 💥 Players with the Most 6s")
players_most_6s = player_shots['6s'].sort_values(ascending=False).head(10)

# HTML styling for tables with improved contrast and center alignment
def generate_centered_table_4s_6s(data, column_name):
    html = f'<table style="width:100%; border-collapse: collapse; text-align: center; font-family: Arial, sans-serif;">'
    html += f'<tr><th style="border: 1px solid #ddd; padding: 10px; background-color: #333; color: #fff;">Player</th><th style="border: 1px solid #ddd; padding: 10px; background-color: #333; color: #fff;">{column_name}</th></tr>'
    for player, value in data.items():
        html += f'<tr><td style="border: 1px solid #ddd; padding: 8px; background-color: #f5f5f5; color: #333;">{player}</td>'
        html += f'<td style="border: 1px solid #ddd; padding: 8px; background-color: #f5f5f5; color: #333;">{value}</td></tr>'
    html += '</table>'
    return html

# Generate and display the table for Players with Most 4s
st.markdown(f"<h3>🔥 Players with the Most 4s</h3>{generate_centered_table_4s_6s(players_most_4s, '4s')}", unsafe_allow_html=True)

# Generate and display the table for Players with Most 6s
st.markdown(f"<h3>💥 Players with the Most 6s</h3>{generate_centered_table_4s_6s(players_most_6s, '6s')}", unsafe_allow_html=True)




# Relationship between Batting Average and Strike Rate in The Oval, London
st.write("### 📈 Relationship between Batting Average and Strike Rate in The Oval, London")
selected_venue = "The Oval, London"
venue_data = data[data['Venue'] == selected_venue]
player_stats = venue_data.groupby('Player').agg({'Runs': 'mean', 'S/R': 'mean'}).reset_index()

plt.figure(figsize=(8, 6))
sns.lineplot(data=player_stats, x='Runs', y='S/R', color='blue', marker='o', markersize=10, markerfacecolor='red', markeredgewidth=1.5)
plt.xlabel('Batting Average', fontsize=12)
plt.ylabel('Strike Rate', fontsize=12)
plt.title('Relationship between Batting Average and Strike Rate in ' + selected_venue, fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
st.pyplot(plt)

# Centuries Scored by Players from Different Teams
st.write("### 🌍 Centuries Scored by Players from Different Teams")
centuries_data = data[data['Runs'] >= 100]
centuries_by_team = centuries_data.groupby('Team')['Player'].count().reset_index()

plt.figure(figsize=(23, 6))
sns.barplot(data=centuries_by_team, x='Team', y='Player', hue='Team', palette='viridis', dodge=False, legend=False)
plt.title('Centuries Scored by Players from Different Teams')
plt.xlabel('Team')
plt.ylabel('Count of Centuries')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
