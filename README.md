# ChatGPT-Football-commentary
This is a automated football commentary module using ChatGPT. This project was conducted under the Project in Data Science at Uppsala University.


DESCRIPTION OF THE FILES
--------------------------
clustering_defensive_lines.py: This file includes clustering player positions, plotting on a pitch, and deriving defensive team formations based on match and frame IDs.

dataframe_creation.py: This file extracts passing events and derives defensive formations based on provided match IDs. It compiles formation, and ball position data into a DataFrame, merging this information with defensive team names and saving it as a CSV file.

import_functions.py: Provided code.

main.py: This file handles user input for frame retrieval and match details, offering options to fetch random frames or input specific match and frame IDs. It then displays extracted match details and generates the Chat-GPT response based on user prompts.

offside.py: This file identifies the attacking and defending teams and checks for potential offside players based on their positions relative to the defensive players.

prompting.py: This defines functionalities to retrieve match details, ball positions, and frame details. It also includes  the generation of a prompt for a particular frame and the passing of the prompt to Chat-GPT to get the response.

settings_gpt.py: This file loads configurations and secrets from a TOML file using a custom function, extracting API, model, and debug parameters used for various functionalities within the code.

statistcs_plot.py: This file performs team formations, ball positions, and various defensive line attributes. It uses provided datasets to create visualizations and statistical insights about team behaviors during matches.

HOW TO RUN
---------------
python main.py

