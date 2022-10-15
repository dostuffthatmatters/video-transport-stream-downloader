import json
import os
import re


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    CONFIG = json.load(f)
    CHUNKLIST_URL = CONFIG["chunklist_url"]
    TITLE = CONFIG["title"]

CHUNKLIST_PATH = os.path.join(PROJECT_DIR, "out", f"{TITLE}.m3u8")
os.system(f"curl {CHUNKLIST_URL} > {CHUNKLIST_PATH}")
with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()

file_pattern = re.compile("[^\n].*_\d+\.ts")
files = re.findall(file_pattern, chunklist)

BASE_URL = "/".join(CHUNKLIST_URL.split("/")[:-1])
os.system(
    "wget " + " ".join([f"{BASE_URL}/{f}" for f in files]) + f" -P {PROJECT_DIR}/out"
)
