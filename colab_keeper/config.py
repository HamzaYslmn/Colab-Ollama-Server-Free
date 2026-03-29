import os
from pathlib import Path

# URL of the Colab notebook to open (can be GitHub Colab link or Drive link)
NOTEBOOK_URL = os.environ.get(
    "COLAB_NOTEBOOK_URL",
    "https://colab.research.google.com/github/HamzaYslmn/Colab-Ollama-Server-Free/blob/main/server.ipynb",
)

# Interval in hours between launches
INTERVAL_HOURS = int(os.environ.get("COLAB_INTERVAL_HOURS", "5"))

# Chrome user data directory to persist login (create once, sign in manually)
CHROME_USER_DATA_DIR = os.environ.get("CHROME_USER_DATA_DIR", str(Path.home() / "colab_chrome_profile"))

# Run headless? (not recommended for login steps)
HEADLESS = os.environ.get("HEADLESS", "0") == "1"

# How long to try to keep the Colab session alive (minutes)
KEEP_ALIVE_MINUTES = int(os.environ.get("KEEP_ALIVE_MINUTES", "290"))

# Page load timeout seconds
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "120"))

# Rotation / copy settings
# How often (hours) to create a new Colab copy and run it (default: 12)
COPY_INTERVAL_HOURS = int(os.environ.get("COLAB_COPY_INTERVAL_HOURS", "12"))

# When creating a copy, wait this many seconds for a new tab/window to appear
COPY_NEW_TAB_WAIT = int(os.environ.get("COLAB_COPY_NEW_TAB_WAIT", "30"))

# Enable automatic copying (set 0 to disable)
ENABLE_AUTO_COPY = os.environ.get("ENABLE_AUTO_COPY", "1") == "1"

