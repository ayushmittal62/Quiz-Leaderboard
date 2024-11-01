import pandas as pd
import streamlit as st

# Define the path to the Excel file on the server
file_path = 'quiz1.xlsx'

# Load the data directly from the file
data = pd.read_excel(file_path)

# Extract necessary columns: Timestamp, Name, Score, Roll Number, Email, Branch
# Ensure these columns exist in the Excel sheet; otherwise, adjust the column names
leaderboard_df = data[['Timestamp', 'Name', 'Score', 'Roll Number', 'Email ID', 'Branch and Year']].copy()

# Convert Timestamp to datetime for proper sorting
leaderboard_df['Timestamp'] = pd.to_datetime(leaderboard_df['Timestamp'])

# Sort by Score (descending) and Timestamp (ascending)
leaderboard_df = leaderboard_df.sort_values(by=['Score', 'Timestamp'], ascending=[False, True])

# Add rank column
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Select final columns for display, including the new columns
leaderboard_df = leaderboard_df[['Rank', 'Name', 'Score', 'Roll Number', 'Email ID', 'Branch and Year']]

# Styling function for the top three ranks
def style_leaderboard(row):
    if row.Rank == 1:
        return ['background-color: gold'] * len(row)
    elif row.Rank == 2:
        return ['background-color: silver'] * len(row)
    elif row.Rank == 3:
        return ['background-color: #cd7f32'] * len(row)
    else:
        return ['background-color: white'] * len(row)

# Apply the custom styling without .hide_index()
styled_df = leaderboard_df.style.apply(style_leaderboard, axis=1)\
                                .set_table_styles([{'selector': 'tr:hover', 'props': [('background-color', '#f1f1f1')]}])\
                                .set_properties(**{'border-color': 'black', 'color': 'black'})

# Streamlit page title and leaderboard display
st.title("E-Cell PIET Presents 🏆 Quiz Competition Leaderboard")
st.write("Top participants rank:")
st.table(styled_df)
