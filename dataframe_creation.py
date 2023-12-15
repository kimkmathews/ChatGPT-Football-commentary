# Authors : Kim Kuruvilla Mathews and Panagiotis Georgios Pennas
# Importing functions from various modules
from offside import load_freeze_frame_data, defending_attacking_team 
from clustering_defensive_lines import classify_and_plot_players_x,structure_of_the_defending_team
from import_functions import pd, load_matches, load_event_data

# Load match data for the specified year and competition
df_matches = load_matches(2022, 808)

formation = []  # List to store formations and ball positions

# Iterate through each match in the DataFrame of matches
for _, matches in df_matches.iterrows():
    match_id = matches['match_id']
    print(match_id)  # Printing the current match ID for tracking
    
    # Extract home and away team IDs for the current match
    home_team_id = matches['home_team_id']
    away_team_id = matches['away_team_id']

    # Load event data for the current match and filter for 'pass' events
    df_events = load_event_data(match_id)
    df_events = df_events[df_events['type'] == 'pass']
    total_frames = 0
    
    frame_list = []
    
    # Load freeze frame data for the current match
    df_frames_match = load_freeze_frame_data(match_id)
    
    formation_counts = {}  # Dictionary to store formation counts

    # Iterate through each event in the event DataFrame
    for _, events in df_events.iterrows():
        total_frames += 1
        frame_id = events['id']
        ball_pos_x, ball_pos_y = events['start_x'], events['start_y']
        
        # Filter frames data for the current event ID
        df_frames = df_frames_match[df_frames_match['id'] == events['id']]
        
        try:
            # Extract attacking and defending team IDs
            attacking_team_id = df_frames['possession_team_id'].unique()[0]
            defending_team_id = df_frames[df_frames['team_id'] != attacking_team_id]['team_id'].unique()[0]
            
            # Check if defending team has 11 players on the field
            if len(df_frames[df_frames['team_id'] == defending_team_id]) == 11:
                # Obtain defending team's formation and ball position for the event
                defending_team_formation = structure_of_the_defending_team(match_id, frame_id)
                
                # Append defending team's formation and ball position to the list
                formation.append((defending_team_formation, ball_pos_x, ball_pos_y))

        except Exception as e:
            # Print error message if an exception occurs during the process
            print(f"Error occurred while saving: {e} - frame_id: {frame_id}")
            pass  # Skipping the operation in case of an error


# Initialize an empty list to store dictionaries
formation_list = []

# Loop through each record in multiple_records
for record in formation:
    # Extract information from the record tuple
    data_tuple, ball_x, ball_y = record
    
    # Restructure the data_tuple into a dictionary
    record_dict = {
        'match_id': data_tuple[0],
        'frame_id': data_tuple[1],
        'defending_team': data_tuple[2],
        'Formation': data_tuple[3],
        'Dist_1_2': data_tuple[4],
        'Dist_2_3': data_tuple[5],
        'Dist_1_3': data_tuple[6],
        'first_line': data_tuple[7],
        'second_line': data_tuple[8],
        'third_line': data_tuple[9],
        'ball_x': ball_x,
        'ball_y': ball_y
    }
    
    # Append the dictionary to the list
    formation_list.append(record_dict)

# Create a DataFrame from the list of dictionaries
df_formation_all = pd.DataFrame(formation_list, columns=['match_id', 'frame_id', 'defending_team', 'Formation', 'Dist_1_2', 'Dist_2_3', 'Dist_1_3', 'first_line','second_line','third_line','ball_x', 'ball_y'])


#Add defensive team name to the dataset

df_matches = load_matches(2022, 808)
unique_teams = df_matches[['home_team_name', 'home_team_id']].drop_duplicates()
unique_teams.columns = ['Team_Name', 'defending_team']
dataset_with_teams = pd.merge(df_formation_all, unique_teams, on='defending_team', how='inner')
dataset_with_teams.drop('Team_Name_x', axis=1, inplace=True)
dataset_with_teams.rename(columns={'Team_Name_y': 'Team_Name'}, inplace=True)

dataset_with_teams.to_csv('dataset_with_teams.csv', index=False) 
