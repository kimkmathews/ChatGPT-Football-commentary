# Author : Kim Kuruvilla Mathews
# Functions : match_details, get_ball_position, get_frame_details, random_frame_gen, prompt_generation

# Authors : Kim Kuruvilla Mathews and Panagiotis Georgios Pennas
# Function : prompting_details
# Data file : feature_prompts.xlsx

# 
# Importing functions from various modules
from import_functions import load_matches, load_event_data, load_freeze_frame_data
from offside import offside_check, defending_attacking_team
from clustering_defensive_lines import classify_and_plot_players_x, structure_of_the_defending_team
from statistcs_plot import information, plot_pitch_information, top_formations, first_third, second_third

import openai
import pandas as pd
from settings_gpt import GPT_BASE, GPT_VERSION, GPT_KEY, ENGINE_GPT

# Configuring OpenAI API settings
openai.api_type = "azure"
openai.api_base = GPT_BASE
openai.api_version = GPT_VERSION
openai.api_key = GPT_KEY

# Function to get match details
def match_details(match_id):
    df_matches = load_matches(2022, 808)
    df_matches_selected = df_matches[df_matches['match_id'] == match_id]
    home_team_id, home_team = df_matches_selected['home_team_id'].iloc[0], df_matches_selected['home_team_name'].iloc[0]
    away_team_id, away_team = df_matches_selected['away_team_id'].iloc[0], df_matches_selected['away_team_name'].iloc[0]

    return home_team_id, home_team, away_team_id, away_team

# Function to get ball position details for a given frame in a match
def get_ball_position(match_id, frame_id):
    df_events = load_event_data(match_id)
    df_events = df_events[df_events['id'] == frame_id]
    ball_pos_x, ball_pos_y = df_events['start_x'].iloc[0], df_events['start_y'].iloc[0]

    # Categorizing ball position into thirds of the pitch
    if ball_pos_x < first_third:
        ball_position = 'first third'
    elif ball_pos_x < second_third and ball_pos_x > first_third:
        ball_position = 'second third'
    else:
        ball_position = 'final third'
    return ball_pos_x, ball_pos_y, ball_position

# Function to get time details for a given frame in a match
def get_frame_details(match_id, frame_id):
    df_events = load_event_data(match_id)
    df_events = df_events[df_events['id'] == frame_id]
    period, minute, second = df_events['period'].iloc[0], df_events['minute'].iloc[0], df_events['second'].iloc[0]

    return period, minute, second

# Function to generate a frame in random 
def random_frame_gen():
    df_matches = load_matches(2022, 808)
    random_match_id = df_matches['match_id'].sample().iloc[0]

    df_events = load_event_data(random_match_id)
    df_events = df_events[df_events['type'] == 'pass']

    df_frames_match = load_freeze_frame_data(random_match_id)

    df_frames_match = df_frames_match[df_frames_match['id'].isin(df_events['id'])]

    df_events = df_events[df_events['id'].isin(df_frames_match['id'])]

    valid_frame_list = []
    for _, frame in df_events.iterrows():
        frame_id = frame['id']
        df_frame = df_frames_match[df_frames_match['id'] == frame_id]
        attacking_team_id, defending_team_id = defending_attacking_team(random_match_id, frame_id)
        if len(df_frame[df_frame['team_id'] == defending_team_id]) == 11:
            valid_frame_list.append(frame_id)
    df_events = df_events[df_events['id'].isin(valid_frame_list)]
    df_events = df_events[df_events['type'] == 'pass']
    random_frame_id = df_events['id'].sample().iloc[0]

    return random_match_id, random_frame_id

# Function to generate a prompt based on the particular frame
def prompting_details(match_id, frame_id):
    home_team_id, home_team, away_team_id, away_team = match_details(match_id)
    attacking_team_id, defending_team_id = defending_attacking_team(match_id, frame_id)

    prompt = ""

    ball_pos_x, ball_pos_y, ball_position = get_ball_position(match_id, frame_id)
    period, minute, second = get_frame_details(match_id, frame_id)

    if period == 1:
        half = 'first'
    elif period == 2:
        half = 'second'

    prompt += f'We are in the {half} half of the game, with {minute} minutes on the clock. '

    if attacking_team_id == home_team_id:
        attacking_team_name = home_team
        defending_team_name = away_team
        prompt += f"Now we have the home team {attacking_team_name} with the ball in their {ball_position} and {defending_team_name} trying to retrieve the ball"
    else:
        attacking_team_name = away_team
        defending_team_name = home_team
        prompt += f"Now we have the away team {attacking_team_name} with the ball in their {ball_position} and {defending_team_name} trying to retrieve the ball"

    frame_offside = offside_check(match_id, frame_id)

    prompt += f" "
    if len(frame_offside) == 0:
        pass
    elif len(frame_offside) == 1:
        for player_info in frame_offside:
            prompt += f"It seems that {player_info['player']} with the number {player_info['jersey_number']} from {attacking_team_name} is in an offside position."

    else:
        for player_info in frame_offside:
            prompt += f"It seems that {attacking_team_name} has {len(frame_offside)} players in an offside position, including {player_info['player']}."

    _, _, _, formation, dist_line_1_2, dist_line_2_3, dist_line_1_3, first_defensive_line, second_defensive_line, third_defensive_line = structure_of_the_defending_team(match_id, frame_id, plot=False)

    team_formation_df = top_formations(defending_team_name, ball_position)

    formation_exists = formation in team_formation_df['Formation'].values

    if formation_exists:
        prompt += f"Now, {defending_team_name} is defending in a {formation} formation, which is a typical formation used by them when the opposition is attacking from the {ball_position}."
        mean_value_first_line, std_dev_value_first_line, _ = information(team_name=defending_team_name, ball_position=ball_position, formation=formation, attribute='first_line', Distribution=False)
        mean_value_dist_1_2, std_dev_value_dist_1_2, _ = information(team_name=defending_team_name, ball_position=ball_position, formation=formation, attribute='Dist_1_2', Distribution=False)
    else:
        prompt += f"Now, {defending_team_name} is defending in a {formation} formation, which is an unusual formation used by them when the opposition is attacking from the {ball_position}."
        mean_value_first_line, std_dev_value_first_line, _ = information(team_name=defending_team_name, ball_position=ball_position, formation='all_formations', attribute='first_line', Distribution=False)
        mean_value_dist_1_2, std_dev_value_dist_1_2, _ = information(team_name=defending_team_name, ball_position=ball_position, formation='all_formations', attribute='Dist_1_2', Distribution=False)

    if first_defensive_line < mean_value_first_line - (std_dev_value_first_line / 2):
        prompt += f"We can see that {defending_team_name} is defending with a deeper defensive line than usual."
    elif first_defensive_line > mean_value_first_line + (std_dev_value_first_line / 2):
        prompt += f"We can see that {defending_team_name} is defending with a higher defensive line than usual."

    if dist_line_1_2 < mean_value_dist_1_2 - (std_dev_value_dist_1_2 / 2):
        prompt += f"Another thing to notice here is that {defending_team_name} is maintaining a tight defensive structure than usual."
    elif dist_line_1_2 > mean_value_dist_1_2 + (std_dev_value_dist_1_2 / 2):
        prompt += f"Another thing to notice here is that {defending_team_name} is maintaining an open defensive structure than usual."

    return prompt

# Function to generate commentary prompt using OpenAI GPT
def prompt_generation(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are an English Football commentator, and you are doing live commentary for a football match. You have to change the given frame description prompt to a commentary-like prompt"
        }]
    # Read the feature_prompts to train the GPT
    feature_prompts = pd.read_excel(f"feature_prompts.xlsx")

    for index, row in feature_prompts.iterrows():
        messages += [{"role": "user", "content": row["user"]}]
        messages += [{"role": "assistant", "content": row['assistant']}]

    messages += [{
        "role": "user",
        "content": prompt
    }]

    # Generate response using OpenAI GPT ChatCompletion API
    response = openai.ChatCompletion.create(
        engine=ENGINE_GPT,  # engine = "deployment_name".
        messages=messages,
        temperature=0.5)

    response_msg = response.choices[0].message.content
    return response_msg
