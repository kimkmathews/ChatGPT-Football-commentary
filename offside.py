# Author : Kim Kuruvilla Mathews
# Importing the load_freeze_frame_data function from import_functions module
from import_functions import load_freeze_frame_data

# Function to determine the attacking and defending teams for a given frame in a match
def defending_attacking_team(match_id, frame_id):
    # Load freeze frame data for the specified match
    df_frames = load_freeze_frame_data(match_id)
    
    # Identify the attacking team based on possession
    attacking_team = df_frames[df_frames['id'] == frame_id]['possession_team_id'].iloc[0]
    
    # Identify the defending team (the team not in possession)
    defending_team = df_frames[(df_frames['id'] == frame_id) & (df_frames['team_id'] != attacking_team)]['team_id'].iloc[0]
    
    return attacking_team, defending_team

# Function to check for offside players in a given frame of a match
def offside_check(match_id, frame_id):
    # Load freeze frame data for the specified match
    df_frames = load_freeze_frame_data(match_id)
    
    # Filter data for the specified frame
    df = df_frames[df_frames['id'] == frame_id]
    
    # Get attacking and defending team IDs
    attacking_team_id, defending_team_id = defending_attacking_team(match_id, frame_id)
    
    # Filter data for players in the attacking team
    df_attacking = df[df['team_id'] == attacking_team_id]
    
    # Get the direction of the attacking team
    attacking_team_dir = df[df['team_id'] == attacking_team_id]['team_direction'].unique()[0]
    
    # List to store offside players
    offside_players = []

    try:
        # Check offside based on the direction of the attacking team
        if attacking_team_dir == 'left':
            attacking_team_pos = df[df['team_id'] == attacking_team_id]['x_signality'].min()
            second_defend_pos = df[df['team_id'] == attacking_team_id]['x_signality'].nsmallest(2).iloc[1]
            ball_position = df[df['player'] == 'ball']['x_signality'].values[0]
            
            # Check if players are offside
            if second_defend_pos > attacking_team_pos and attacking_team_pos < ball_position:
                for _, attacking_player in df_attacking.iterrows():
                    if attacking_player['x_signality'] < second_defend_pos:
                        offside_players.append({'jersey_number': attacking_player['jersey_number'], 'player': attacking_player['player']})
        elif attacking_team_dir == 'right':
            attacking_team_pos = df[df['team_id'] == attacking_team_id]['x_signality'].max()
            second_defend_pos = df[df['team_id'] == attacking_team_id]['x_signality'].nlargest(2).iloc[1]
            ball_position = df[df['player'] == 'ball']['x_signality'].values[0]
            
            # Check if players are offside
            if second_defend_pos < attacking_team_pos and attacking_team_pos > ball_position:
                for _, attacking_player in df_attacking.iterrows():
                    if attacking_player['x_signality'] > second_defend_pos:
                        offside_players.append({'jersey_number': attacking_player['jersey_number'], 'player': attacking_player['player']})
    except Exception as e:
        # Handle exceptions
        pass
    
    return offside_players