import pandas as pd
import streamlit as st

# Load both quiz files
quiz1_path = 'quiz2.xlsx'
quiz2_path = 'quiz3.xlsx'

# Load the data from both quizzes
quiz1_data = pd.read_excel(quiz1_path, dtype={'Roll Number': str})  # Load Roll Number as string
quiz2_data = pd.read_excel(quiz2_path, dtype={'Roll Number': str})  # Load Roll Number as string

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
quiz1_data = quiz1_data.rename(columns={'Score': 'Score_Quiz1', 'Timestamp': 'Timestamp_Quiz1'})
quiz2_data = quiz2_data.rename(columns={'Score': 'Score_Quiz2', 'Timestamp': 'Timestamp_Quiz2'})

# Merge datasets on Name and Roll Number, using outer join to include all participants
leaderboard_df = pd.merge(
    quiz1_data, quiz2_data, on=['Name', 'Roll Number'], how='outer'
)

# Remove duplicate entries if they exist based on 'Name' and 'Roll Number'
leaderboard_df = leaderboard_df.drop_duplicates(subset=['Name', 'Roll Number'])

# Fill missing scores with 0 for participants who took only one quiz and convert scores to integer
leaderboard_df['Score_Quiz1'] = leaderboard_df['Score_Quiz1'].fillna(0).astype(int)
leaderboard_df['Score_Quiz2'] = leaderboard_df['Score_Quiz2'].fillna(0).astype(int)

# Calculate total score and convert it to integer
leaderboard_df['Total_Score'] = (leaderboard_df['Score_Quiz1'] + leaderboard_df['Score_Quiz2']).astype(int)

# Sort by Total Score (descending) and Earliest Timestamp (ascending)
leaderboard_df = leaderboard_df.sort_values(by=['Total_Score', 'Timestamp_Quiz1', 'Timestamp_Quiz2'], ascending=[False, True, True])

# Add ranking
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Select final columns for display
final_leaderboard = leaderboard_df[['Rank', 'Name', 'Roll Number', 'Score_Quiz1', 'Score_Quiz2', 'Total_Score']]

# Display in Streamlit without index column
st.title("Final Scores for Both Quizzes")
st.write("Rankings based on the total score:")

# Use st.dataframe to display the table, increase size of the table box
st.dataframe(final_leaderboard.set_index('Rank'), height=600, width=900)
