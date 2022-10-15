import json
import os
import re


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "out")
with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    CONFIG = json.load(f)
    CHUNKLIST_URL = CONFIG["chunklist_url"]
    TITLE = CONFIG["title"]

# TODO: Do not download a chunklist that is already cached
CHUNKLIST_PATH = os.path.join(DATA_DIR, f"{TITLE}.m3u8")
os.system(f"curl {CHUNKLIST_URL} > {CHUNKLIST_PATH}")
with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()

file_pattern = re.compile("[^\n].*_\d+\.ts")
files = re.findall(file_pattern, chunklist)

# TODO: Do not download files that have already been cached
BASE_URL = "/".join(CHUNKLIST_URL.split("/")[:-1])
os.system(
    "wget " + " ".join([f"{BASE_URL}/{f}" for f in files]) + f" -P {PROJECT_DIR}/out"
)

# TODO: cat streams into one all.ts
# TODO: convert all.ts into mp4
