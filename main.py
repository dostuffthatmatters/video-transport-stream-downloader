import json
import os
import re


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    CONFIG = json.load(f)

DATA_DIR = os.path.join(PROJECT_DIR, "out")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CHUNKLIST_URL = CONFIG["chunklist_url"]
TITLE = CONFIG["title"]
CHUNKLIST_PATH = os.path.join(DATA_DIR, f"{TITLE}-chunklist.m3u8")
BASE_URL = "/".join(CHUNKLIST_URL.split("/")[:-1])

# TODO: Do not download a chunklist that is already cached
os.system(f"curl {CHUNKLIST_URL} > {CHUNKLIST_PATH}")
with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()

file_pattern = re.compile("[^\n].*_\d+\.ts")
files = re.findall(file_pattern, chunklist)
missing_files = [f for f in files if not os.path.isfile(RAW_DATA_DIR, f)]
file_urls = [f"{BASE_URL}/{f}" for f in missing_files]
os.system("wget " + " ".join(file_urls) + f" -P {RAW_DATA_DIR}")

# TODO: cat streams into one all.ts
# TODO: convert all.ts into mp4
