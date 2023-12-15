#Author : Panagiotis Georgios Pennas
#Function : classify_and_plot_players_x,structure_of_the_defending_team

# Importing necessary libraries
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Importing functions from other modules
from offside import load_freeze_frame_data, defending_attacking_team 
from import_functions import pd, load_matches, load_event_data


# Function to classify players based on their x-positions and plot the result
def classify_and_plot_players_x(x_positions, y_positions, team_direction, team, pitch_length=106, pitch_width=68, plot=False):
    # Applying KMeans clustering to x-positions
    kmeans = KMeans(n_clusters=3)
    x_positions = [[x] for x in x_positions]  
    kmeans.fit(x_positions)
    labels = kmeans.labels_

    # Plotting the pitch lines if requested
    if plot:
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.plot([0, 0], [0, pitch_width], color='black')  
        plt.plot([0, pitch_length], [pitch_width, pitch_width], color='black')  
        plt.plot([pitch_length, pitch_length], [pitch_width, 0], color='black')  
        plt.plot([pitch_length, 0], [0, 0], color='black')  
        plt.plot([pitch_length/2, pitch_length/2], [0, pitch_width], color='black')  

    # Initializing and organizing player clusters
    clusters = {0: [], 1: [], 2: []}
    for i, (x, y) in enumerate(zip(x_positions, y_positions)):
        clusters[labels[i]].append((x[0], y))

    # Calculating distances and sorting clusters based on distance
    distances = {}
    for cluster, players in clusters.items():
        xs, _ = zip(*players)
        centroid_x = np.mean(xs)
        distance = np.abs(centroid_x)
        distances[cluster] = distance

    if team_direction == 'left':
        sorted_clusters = sorted(distances, key=lambda x: distances[x], reverse=True)
    else:
        sorted_clusters = sorted(distances, key=lambda x: distances[x])

    # Plotting player clusters on the pitch
    for cluster in sorted_clusters:
        players = clusters[cluster]
        xs, ys = zip(*players)
        centroid_x = np.mean(xs)
        centroid_y = np.mean(ys)
        if plot:
            circle = plt.Circle((centroid_x, centroid_y), 5, color='none', edgecolor='black')
            ax.add_patch(circle)
            plt.scatter(xs, ys, label=f'Cluster {cluster}', alpha=0.7)

    # Reordering clusters for further analysis
    reordered_clusters = {k: clusters[k] for k in sorted_clusters}

    # Extracting x-positions for each cluster
    clusters_x = {0: [], 1: [], 2: []}
    for i, x in enumerate((x_positions)):
        clusters_x[labels[i]].append(x[0])

    # Calculating average and maximum x-positions for defensive line analysis
    avg_of_1_line = np.mean(clusters_x[0])
    avg_of_2_line = np.mean(clusters_x[1])
    avg_of_3_line = np.mean(clusters_x[2])

    max_of_1_line = max(clusters_x[0])
    min_of_2_line = min(clusters_x[1])
    max_of_2_line = max(clusters_x[1])
    min_of_3_line = min(clusters_x[2])

    # Calculating distances between lines
    dist_line_1_2 = np.abs(avg_of_1_line - avg_of_2_line)
    dist_line_2_3 = np.abs(avg_of_2_line - avg_of_3_line)
    dist_line_1_3 = np.abs(avg_of_1_line - avg_of_3_line)

    # Calculating defensive line positions
    first_defensive_line = pitch_length - avg_of_1_line if team_direction == 'left' else avg_of_1_line
    second_defensive_line = pitch_length - avg_of_2_line if team_direction == 'left' else avg_of_2_line
    third_defensive_line = pitch_length - avg_of_3_line if team_direction == 'left' else avg_of_3_line

    # Calculating formation based on player counts in each cluster
    counts = [len(reordered_clusters[0]), len(reordered_clusters[1]), len(reordered_clusters[2])]
    formation = f"{counts[0]}-{counts[1]}-{counts[2]}"

    # Plotting additional pitch lines if requested
    if plot:
        y_lines = pitch_width / 3
        y1_line = y_lines
        y2_line = y_lines * 2
        plt.plot([avg_of_1_line, avg_of_1_line], [0, pitch_width], color='red', linestyle='dashed')
        plt.plot([avg_of_2_line, avg_of_2_line], [0, pitch_width], color='orange', linestyle='dashed')
        plt.plot([avg_of_3_line, avg_of_3_line], [0, pitch_width], color='green', linestyle='dashed')
        plt.plot([0, pitch_length], [y1_line, y1_line], color='red', linestyle='dashed')
        plt.plot([0, pitch_length], [y2_line, y2_line], color='red', linestyle='dashed')
        plt.title('Players Categorized by Position Clusters (Based on X-axis only)')
        plt.xlabel('Length (m)')
        plt.ylabel('Width (m)')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlim(0, pitch_length)
        plt.ylim(0, pitch_width)
        plt.legend()
        plt.show()

    return formation, dist_line_1_2, dist_line_2_3, dist_line_1_3, first_defensive_line, second_defensive_line, third_defensive_line

# Function to analyze the structure of the defending team
def structure_of_the_defending_team(match_id, frame_id, plot=False):
    # Loading freeze frame data for the match
    df_frames = load_freeze_frame_data(match_id)
    
    # Filtering the frame from DataFrame df_frames based on frame_id
    df = df_frames[df_frames['id'] == frame_id]
    
    # Extracting defending team ID
    _, defending_team_id = defending_attacking_team(match_id, frame_id)
    
    # Filtering the defending team's data from the frame
    df_defending = df[df['team_id'] == defending_team_id]
    
    # Excluding the goalkeeper from the defending team's data
    df_defending = df_defending[df_defending['role'] != 1]
    
    # Extracting specific position attributes for the defending team
    df_defending = df_defending.loc[:, ["x_adjusted", "y_adjusted", "team_direction", "team"]]
    
    # Extracting team and team_direction for further analysis
    team = df_defending["team"].unique()[0]
    team_direction = df_defending["team_direction"].unique()[0]
    
    # Adjusting positions based on team direction
    df_defending.loc[df_defending["team_direction"] != "right", "x_adjusted"] = 106 - df_defending.loc[df_defending["team_direction"] != "right", "x_adjusted"]
    df_defending.loc[df_defending["team_direction"] != "right", "y_adjusted"] = 68 - df_defending.loc[df_defending["team_direction"] != "right", "y_adjusted"]

    # Calling the previous function 'classify_and_plot_players_x' for further analysis
    formation, dist_line_1_2, dist_line_2_3, dist_line_1_3, first_defensive_line, second_defensive_line, third_defensive_line = classify_and_plot_players_x(
        df_defending["x_adjusted"], df_defending["y_adjusted"], team_direction, team, pitch_length=106, pitch_width=68, plot=plot)

    # Returning relevant data
    return match_id, frame_id, defending_team_id, formation, dist_line_1_2, dist_line_2_3, dist_line_1_3, first_defensive_line, second_defensive_line, third_defensive_line
