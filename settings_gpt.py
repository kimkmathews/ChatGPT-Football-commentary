# Inspired by already provided code
# Modified by : Kim Kuruvilla Mathews
import os
import toml

# Function to load secrets from a TOML file
def load_secrets(filename):
    with open(filename, "r") as file:
        secrets = toml.load(file)
    return secrets

# Load credentials from the secrets file
secrets = load_secrets("secrets.toml")

# Extract GPT parameters
API_URL = secrets["API_URL"]
LOCAL_API_URL = secrets["LOCAL_API_URL"]
TOKEN = secrets["TOKEN"]
GPT_BASE = secrets["GPT_BASE"]
GPT_VERSION = secrets["GPT_VERSION"]
GPT_KEY = secrets["GPT_KEY"]

# Extract model parameters
ENGINE_ADA = secrets["ENGINE_ADA"]
ENGINE_GPT = secrets["ENGINE_GPT"]
EMBEDDING_MODEL = secrets["EMBEDDING_MODEL"]
GPT_MODEL = secrets["GPT_MODEL"]


DEBUG = True





# In[ ]:




