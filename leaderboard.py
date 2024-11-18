import pandas as pd
import streamlit as st
from pathlib import Path

# Create two columns for logo and "Team Astrive" title
col1, col2 = st.columns([1, 3])

# Load and display the logo in the first column
logo_path = 'logo.png'  # Update to the correct path for your logo file
with col1:
    if Path(logo_path).is_file():
        st.image(logo_path, width=100)  # Adjust width as needed
    else:
        st.write("Logo file not found.")

# Display "Team Astrive" title in the second column
with col2:
    st.markdown("<h1 style='text-align: left; color: white;'>Team Astrive</h1>", unsafe_allow_html=True)

# Add the main leaderboard title below the logo and "Team Astrive"
st.markdown("<h2 style='text-align: center; color: white;'>E-Cell PIET Presents 🏆 Quiz Leaderboard</h2>", unsafe_allow_html=True)

# Load Week 1 quiz files
quiz1_path = 'quiz111.xlsx'  # Week 1 File 1
quiz2_path = 'quiz22.xlsx'   # Week 1 File 2

# Load Week 2 quiz file (provided by the user)
quiz3_path = 'quiz3.xlsx'  # Week 2 File

# Load Week 1 data
quiz1_data = pd.read_excel(quiz1_path, dtype={'Roll Number': str})
quiz2_data = pd.read_excel(quiz2_path, dtype={'Roll Number': str})

# Remove unnamed columns
quiz1_data = quiz1_data.loc[:, ~quiz1_data.columns.str.contains('^Unnamed')]
quiz2_data = quiz2_data.loc[:, ~quiz2_data.columns.str.contains('^Unnamed')]

# Standardize Week 1 columns
quiz1_data = quiz1_data[['Roll Number', 'Name', 'Score']].copy()
quiz2_data = quiz2_data[['Roll Number', 'Name', 'Score']].copy()

# Rename scores for clarity
quiz1_data = quiz1_data.rename(columns={'Score': 'Score_Quiz1'})
quiz2_data = quiz2_data.rename(columns={'Score': 'Score_Quiz2'})

# Merge Week 1 data on Roll Number and calculate Week 1 total score
week1_data = pd.merge(
    quiz1_data, quiz2_data, on='Roll Number', how='outer'
)

# Handle names: Prefer names from the first quiz; if not available, take from the second quiz
week1_data['Name'] = week1_data['Name_x'].combine_first(week1_data['Name_y'])

# Drop intermediate columns after merging
week1_data = week1_data[['Roll Number', 'Name', 'Score_Quiz1', 'Score_Quiz2']]
week1_data['Score_Quiz1'] = week1_data['Score_Quiz1'].fillna(0).astype(int)
week1_data['Score_Quiz2'] = week1_data['Score_Quiz2'].fillna(0).astype(int)
week1_data['Week_1_Score'] = week1_data['Score_Quiz1'] + week1_data['Score_Quiz2']

# Drop intermediate score columns
week1_data = week1_data[['Roll Number', 'Name', 'Week_1_Score']]

# Load Week 2 data
week2_data = pd.read_excel(quiz3_path, dtype={'Roll Number': str})
week2_data = week2_data.loc[:, ~week2_data.columns.str.contains('^Unnamed')]
week2_data = week2_data[['Roll Number', 'Name', 'Score']].copy()
week2_data = week2_data.rename(columns={'Score': 'Week_2_Score'})

# Merge Week 1 and Week 2 data
leaderboard_df = pd.merge(
    week1_data, week2_data, on='Roll Number', how='outer'
)

# Handle names: Prefer names from Week 1; if not available, take from Week 2
leaderboard_df['Name'] = leaderboard_df['Name_x'].combine_first(leaderboard_df['Name_y'])

# Fill missing scores with 0
leaderboard_df['Week_1_Score'] = leaderboard_df['Week_1_Score'].fillna(0).astype(int)
leaderboard_df['Week_2_Score'] = leaderboard_df['Week_2_Score'].fillna(0).astype(int)

# Calculate total score
leaderboard_df['Total_Score'] = leaderboard_df['Week_1_Score'] + leaderboard_df['Week_2_Score']

# Remove duplicate Roll Number entries, keeping the one with the highest Total_Score
leaderboard_df = leaderboard_df.sort_values(by=['Total_Score'], ascending=False)
leaderboard_df = leaderboard_df.drop_duplicates(subset=['Roll Number'], keep='first')

# Add ranking
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Final leaderboard columns
final_leaderboard = leaderboard_df[['Rank', 'Roll Number', 'Name', 'Week_1_Score', 'Week_2_Score', 'Total_Score']]

# Display the leaderboard
st.dataframe(final_leaderboard.set_index('Rank'), height=600, width=900)
