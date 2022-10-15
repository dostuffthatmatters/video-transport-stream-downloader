import json
import os


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    CONFIG = json.load(f)
    CHUNKLIST_URL = CONFIG["chunklist_url"]
    TITLE = CONFIG["title"]

CHUNKLIST_PATH = os.path.join(PROJECT_DIR, "out", f"{TITLE}.m3u8")
os.system(f"curl {CHUNKLIST_URL} > {CHUNKLIST_PATH}")
with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()
