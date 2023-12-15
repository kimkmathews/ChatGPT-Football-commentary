# Author : Panagiotis Georgios Pennas
# Functions : information, plot_pitch_information

# Author : Kim Kuruvilla Mathews
# Function : top_formations
# Importing necessary functions from import_functions module
from import_functions import *

# Reading dataset with teams from a CSV file
dataset_with_teams = pd.read_csv('dataset_with_teams.csv')

# Constants for pitch thirds
first_third = 35.33
second_third = 70.66

# Function to gather information based on specified parameters
def information(team_name='all_teams', ball_position='everywhere', formation='all_formations', attribute='first_line', Distribution=False):
    
    # Filtering data based on team_name
    if team_name == 'all_teams':
        data1 = dataset_with_teams
    else:
        data1 = dataset_with_teams[dataset_with_teams['Team_Name'] == team_name]
    
    # Filtering data based on ball_position
    if ball_position == 'everywhere':
        data2 = data1
    elif ball_position == 'first third':
        data2 = data1[data1['ball_x'] < first_third]
    elif ball_position == 'second third':
        data2 = data1[(data1['ball_x'] < second_third) & (data1['ball_x'] > first_third)]
    else:
        data2 = data1[data1['ball_x'] > second_third]

    # Filtering data based on formation
    if formation == 'all_formations':
        data3 = data2
    else:
        data3 = data2[data2['Formation'] == formation]
    
    # Extracting data for distribution
    data_for_distribution = data3[attribute]
    
    # Calculating mean and standard deviation
    mean_value = data_for_distribution.mean()
    std_dev_value = data_for_distribution.std()
    
    # Plotting distribution if Distribution parameter is True
    if Distribution:
        plt.figure(figsize=(12, 6))
        sns.displot(data_for_distribution, bins=100)

        plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
        plt.axvline(mean_value - std_dev_value, color='orange', linestyle='dashed', linewidth=2, label=f'Mean - Std Dev: {mean_value - std_dev_value:.2f}')
        plt.axvline(mean_value + std_dev_value, color='green', linestyle='dashed', linewidth=2, label=f'Mean + Std Dev: {mean_value + std_dev_value:.2f}')

        plt.title(f'Distribution of {attribute} for Formation {formation} for team {team_name} when the ball is {ball_position}')
        plt.xlabel('Dist_1_2')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    return mean_value, std_dev_value, team_name

# Function to plot pitch information and compare defensive lines
def plot_pitch_information(team_name_1, team_name_2, ball_position, formation, attribute, distribution):
    if attribute in ['first_line', 'second_line', 'third_line']:
        # Get information for the first team
        mean_one_team, std_one_team, team_name = information(team_name_1, ball_position=ball_position, formation=formation, attribute=attribute, Distribution=distribution)
        
        # Get information for all teams
        mean_all_teams, std_all_teams, team_name1 = information(team_name_2, ball_position=ball_position, formation=formation, attribute=attribute, Distribution=distribution)

        # Set up the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.plot([0, 0], [0, pitch_width], color='black')  # left line
        plt.plot([0, pitch_length], [pitch_width, pitch_width], color='black')  # top line
        plt.plot([pitch_length, pitch_length], [pitch_width, 0], color='black')  # right line
        plt.plot([pitch_length, 0], [0, 0], color='black')  # bottom line
        plt.plot([pitch_length / 2, pitch_length / 2], [0, pitch_width], color='black')  # half-way 

        # Highlight ball position
        if ball_position != "everywhere":
            if ball_position == 'first third':
                plt.plot([pitch_length - first_third, pitch_length - first_third], [0, pitch_width], color='lightgreen', linestyle='solid')
                plt.fill_betweenx([0, pitch_width], pitch_length - first_third, pitch_length, color='lightgreen', alpha=0.5, label='Ball position')
            elif ball_position == 'second third':
                plt.plot([pitch_length - second_third, pitch_length - second_third], [0, pitch_width], color='lightgreen', linestyle='solid')
                plt.fill_betweenx([0, pitch_width], pitch_length - second_third, pitch_length - first_third, color='lightgreen', alpha=0.5, label='Ball position')
            else:
                plt.plot([first_third, first_third], [0, pitch_width], color='lightgreen', linestyle='solid')
                plt.fill_betweenx([0, pitch_width], 0, first_third, color='lightgreen', alpha=0.5, label='Ball position')

        # Plot mean average_first_line for both teams
        plt.plot([mean_one_team, mean_one_team], [0, pitch_width], color='yellow', linestyle='solid', label=f'Mean for {team_name}')
        plt.plot([mean_all_teams, mean_all_teams], [0, pitch_width], color='blue', linestyle='solid', label=f'Mean for {team_name1}')

        mean_plus_std_all_teams = mean_all_teams + std_all_teams
        plt.plot([mean_plus_std_all_teams, mean_plus_std_all_teams], [0, pitch_width], color='green', linestyle='dashed', label=f'Mean + Std Dev')

        mean_minus_std_all_teams = mean_all_teams - std_all_teams
        plt.plot([mean_minus_std_all_teams, mean_minus_std_all_teams], [0, pitch_width], color='red', linestyle='dashed', label=f'Mean - Std Dev')

        # Fill between the lines
        if team_name_1 == "all_teams" or team_name_2 == "all_teams":
            plt.fill_betweenx([0, pitch_width], mean_minus_std_all_teams, mean_plus_std_all_teams, color='lightgray', alpha=0.5, label='Std Dev Range')

        # Customize the plot
        plt.title('Comparison of defensive lines')
        plt.xlabel('Length (m)')
        plt.ylabel('Width (m)')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlim(0, pitch_length)
        plt.ylim(0, pitch_width)
        plt.legend()

        # Show the plot
        plt.show()
    else: 
        # If the attribute is not one of the defensive lines, plot the distribution
        mean_one_team, std_one_team, team_name = information(team_name_1, ball_position=ball_position, formation=formation, attribute=attribute, Distribution=True)
        mean_all_teams, std_all_teams, team_name1 = information(team_name_2, ball_position=ball_position, formation=formation, attribute=attribute, Distribution=True)

# Function to analyze top formations based on team and ball position
def top_formations(team_name, ball_position):

    df_team = dataset_with_teams[dataset_with_teams['Team_Name'] == team_name]

    if ball_position == 'first third':
        df_first_line = df_team[df_team['ball_x'] < first_third]
        top_formations = df_first_line.groupby('Team_Name')['Formation'].value_counts().groupby(level=0).nlargest(5).reset_index(level=1, drop=True)
        average_distances_1_2 = df_first_line.groupby(['Team_Name', 'Formation'])['Dist_1_2'].mean()
        average_distances_2_3 = df_first_line.groupby(['Team_Name', 'Formation'])['Dist_2_3'].mean()
        average_distances_1_3 = df_first_line.groupby(['Team_Name', 'Formation'])['Dist_1_3'].mean()

        average_first_line = df_first_line.groupby(['Team_Name', 'Formation'])['first_line'].mean()
        average_second_line = df_first_line.groupby(['Team_Name', 'Formation'])['second_line'].mean()
        average_third_line = df_first_line.groupby(['Team_Name', 'Formation'])['third_line'].mean()

        result_df_first_line = pd.DataFrame({'Top_Formations': top_formations,
                                             'Average_Dist_1_2': average_distances_1_2,
                                             'Average_Dist_2_3': average_distances_2_3,
                                             'Average_Dist_1_3': average_distances_1_3,
                                             'Average_First_line': average_first_line,
                                             'Average_Second_line': average_second_line,
                                             'Average_Third_line': average_third_line}).reset_index()
        result_df_first_line = result_df_first_line.dropna().reset_index(drop=True)
        return result_df_first_line
    elif ball_position == 'second third':
        df_second_line = df_team[(df_team['ball_x'] < second_third) & (df_team['ball_x'] > first_third)]
        top_formations = df_second_line.groupby('Team_Name')['Formation'].value_counts().groupby(level=0).nlargest(5).reset_index(level=1, drop=True)
        average_distances_1_2 = df_second_line.groupby(['Team_Name', 'Formation'])['Dist_1_2'].mean()
        average_distances_2_3 = df_second_line.groupby(['Team_Name', 'Formation'])['Dist_2_3'].mean()
        average_distances_1_3 = df_second_line.groupby(['Team_Name', 'Formation'])['Dist_1_3'].mean()

        average_first_line = df_second_line.groupby(['Team_Name', 'Formation'])['first_line'].mean()
        average_second_line = df_second_line.groupby(['Team_Name', 'Formation'])['second_line'].mean()
        average_third_line = df_second_line.groupby(['Team_Name', 'Formation'])['third_line'].mean()

        result_df_second_line = pd.DataFrame({'Top_Formations': top_formations,
                                              'Average_Dist_1_2': average_distances_1_2,
                                              'Average_Dist_2_3': average_distances_2_3,
                                              'Average_Dist_1_3': average_distances_1_3,
                                              'Average_First_line': average_first_line,
                                              'Average_Second_line': average_second_line,
                                              'Average_Third_line': average_third_line}).reset_index()
        result_df_second_line = result_df_second_line.dropna().reset_index(drop=True)
        return result_df_second_line
    else:
        df_third_line = df_team[df_team['ball_x'] > second_third]
        top_formations = df_third_line.groupby('Team_Name')['Formation'].value_counts().groupby(level=0).nlargest(5).reset_index(level=1, drop=True)
        average_distances_1_2 = df_third_line.groupby(['Team_Name', 'Formation'])['Dist_1_2'].mean()
        average_distances_2_3 = df_third_line.groupby(['Team_Name', 'Formation'])['Dist_2_3'].mean()
        average_distances_1_3 = df_third_line.groupby(['Team_Name', 'Formation'])['Dist_1_3'].mean()

        average_first_line = df_third_line.groupby(['Team_Name', 'Formation'])['first_line'].mean()
        average_second_line = df_third_line.groupby(['Team_Name', 'Formation'])['second_line'].mean()
        average_third_line = df_third_line.groupby(['Team_Name', 'Formation'])['third_line'].mean()

        result_df_third_line = pd.DataFrame({'Top_Formations': top_formations,
                                             'Average_Dist_1_2': average_distances_1_2,
                                             'Average_Dist_2_3': average_distances_2_3,
                                             'Average_Dist_1_3': average_distances_1_3,
                                             'Average_First_line': average_first_line,
                                             'Average_Second_line': average_second_line,
                                             'Average_Third_line': average_third_line}).reset_index()
        result_df_third_line = result_df_third_line.dropna().reset_index(drop=True)
        return result_df_third_line
