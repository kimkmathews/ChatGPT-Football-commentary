# Extracted from code provided by Supervisor
# Importing necessary libraries
import os
import traceback
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Importing helper functions for visualizations
#from helpers.vizualizations import *
from settings import ROOT_DIR

# Suppressing warnings
import warnings
warnings.filterwarnings('ignore')

# Constants for pitch dimensions
pitch_length = 106
pitch_width = 68

# Below functions are already provided code
# Function to load match data
def load_matches(season, competition):
    try:
        # Reading match data from parquet file
        ret = pd.read_parquet(f"{ROOT_DIR}/data/matches_{season}_{competition}.parquet")

        # Temporary
        # Ignore matches without events/freeze frames
        existing_matches_events = [int(x.split('.')[0]) for x in os.listdir(f"{ROOT_DIR}/data/events/")]
        ret = ret[ret['match_id'].isin(existing_matches_events)]

        existing_matches_freeze_frames = [int(x.split('.')[0]) for x in os.listdir(f"{ROOT_DIR}/data/freeze_frames/")]
        ret = ret[ret['match_id'].isin(existing_matches_freeze_frames)]

        return ret

    except Exception as err:
        traceback.print_exc()

    return None

# Function to load event data for a specific match
def load_event_data(match_id):
    try:
        # Reading event data from parquet file
        ret = pd.read_parquet(f"{ROOT_DIR}/data/events/{match_id}.parquet").reset_index(drop=True)

        # Transforming coordinates based on pitch dimensions
        def transform_x_coordinates(start_x, pitch_length=pitch_length):
            return (start_x / 100) * pitch_length

        def transform_y_coordinates(start_x, pitch_width=pitch_width):
            return pitch_width - ((start_x / 100) * pitch_width)

        ret['start_x'] = [transform_x_coordinates(x) for x in ret['start_x']]
        ret['start_y'] = [transform_y_coordinates(x) for x in ret['start_y']]

        # -1 are default values for missing coordinates, not transformed
        ret['end_x'] = [-1 if x == -1 else transform_x_coordinates(x) for x in ret['end_x']]
        ret['end_y'] = [-1 if x == -1 else transform_y_coordinates(x) for x in ret['end_y']]

        return ret

    except Exception as err:
        traceback.print_exc()

    return None

# Function to load freeze frame data for a specific match
def load_freeze_frame_data(match_id):
    try:
        # Reading freeze frame data from parquet file
        ret = pd.read_parquet(f"{ROOT_DIR}/data/freeze_frames/{match_id}.parquet")

        return ret

    except Exception as err:
        traceback.print_exc()

    return None
