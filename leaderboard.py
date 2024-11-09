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

# Load both quiz files
quiz1_path = 'quiz11.xlsx'
quiz2_path = 'quiz22.xlsx'

# Load the data from both quizzes
quiz1_data = pd.read_excel(quiz1_path, dtype={'Roll Number': str})
quiz2_data = pd.read_excel(quiz2_path, dtype={'Roll Number': str})

# Remove unnamed columns if present
quiz1_data = quiz1_data.loc[:, ~quiz1_data.columns.str.contains('^Unnamed')]
quiz2_data = quiz2_data.loc[:, ~quiz2_data.columns.str.contains('^Unnamed')]

# Standardize columns for merging
quiz1_data = quiz1_data[['Timestamp', 'Name', 'Score', 'Roll Number']].copy()
quiz2_data = quiz2_data[['Timestamp', 'Name', 'Score', 'Roll Number']].copy()

# Convert Timestamp to datetime for accurate merging and sorting
quiz1_data['Timestamp'] = pd.to_datetime(quiz1_data['Timestamp'])
quiz2_data['Timestamp'] = pd.to_datetime(quiz2_data['Timestamp'])

# Rename score columns to differentiate between quizzes
quiz1_data = quiz1_data.rename(columns={'Score': 'Score_Quiz1', 'Timestamp': 'Timestamp_Quiz1', 'Name': 'Name_Quiz1'})
quiz2_data = quiz2_data.rename(columns={'Score': 'Score_Quiz2', 'Timestamp': 'Timestamp_Quiz2', 'Name': 'Name_Quiz2'})

# Merge datasets on Roll Number only, using outer join to include all participants
leaderboard_df = pd.merge(
    quiz1_data, quiz2_data, on='Roll Number', how='outer'
)

# Handle name columns: Combine names from both quizzes where possible, otherwise use available name
leaderboard_df['Name'] = leaderboard_df['Name_Quiz1'].combine_first(leaderboard_df['Name_Quiz2'])

# Drop the separate Name columns after combining
leaderboard_df = leaderboard_df.drop(columns=['Name_Quiz1', 'Name_Quiz2'])

# Fill missing scores with 0 for participants who took only one quiz and convert scores to integer
leaderboard_df['Score_Quiz1'] = leaderboard_df['Score_Quiz1'].fillna(0).astype(int)
leaderboard_df['Score_Quiz2'] = leaderboard_df['Score_Quiz2'].fillna(0).astype(int)

# Calculate total score and convert it to integer
leaderboard_df['Total_Score'] = (leaderboard_df['Score_Quiz1'] + leaderboard_df['Score_Quiz2']).astype(int)

# Drop duplicate Roll Number entries, keeping the row with the highest Total_Score or latest Timestamp
leaderboard_df = leaderboard_df.sort_values(by=['Total_Score', 'Timestamp_Quiz1', 'Timestamp_Quiz2'], ascending=[False, True, True])
leaderboard_df = leaderboard_df.drop_duplicates(subset=['Roll Number'], keep='first')

# Add ranking
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Select final columns for display
final_leaderboard = leaderboard_df[['Rank', 'Name', 'Roll Number', 'Score_Quiz1', 'Score_Quiz2', 'Total_Score']]

# Display in Streamlit without index column
# Use st.dataframe to display the table, increase size of the table box
st.dataframe(final_leaderboard.set_index('Rank'), height=600, width=900)
