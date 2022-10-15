import json
import os
import re
import shutil


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PROJECT_DIR, "config.json")) as f:
    CONFIG = json.load(f)

DATA_DIR = os.path.join(PROJECT_DIR, "out")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

CHUNKLIST_URL = CONFIG["chunklist_url"]
TITLE = CONFIG["title"]
CHUNKLIST_PATH = os.path.join(DATA_DIR, f"{TITLE}-chunklist.m3u8")
MERGED_TS_PATH = os.path.join(DATA_DIR, f"{TITLE}-merged.ts")
MERGED_MP4_PATH = os.path.join(DATA_DIR, f"{TITLE}-merged.mp4")
BASE_URL = "/".join(CHUNKLIST_URL.split("/")[:-1])

# download the chunklist
os.system(f"curl {CHUNKLIST_URL} > {CHUNKLIST_PATH}")
with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()
os.remove(CHUNKLIST_PATH)

# download all ts files
file_pattern = re.compile("[^\n].*_\d+\.ts")
files = re.findall(file_pattern, chunklist)
file_urls = [f"{BASE_URL}/{f}" for f in files]
os.system("wget " + " ".join(file_urls) + f" -P {RAW_DATA_DIR}")

# merge all ts files into one ts file + delete individual ts files
raw_ts_files = [os.path.join(RAW_DATA_DIR, f) for f in files]
os.system(f"cat " + " ".join(raw_ts_files) + f" > {MERGED_TS_PATH}")
shutil.rmtree(RAW_DATA_DIR)

# convert the merged ts file into an mp4 file + delete merged ts file
if os.path.isfile(MERGED_MP4_PATH):
    os.remove(MERGED_MP4_PATH)
os.system(f"ffmpeg -i {MERGED_TS_PATH} -acodec copy -vcodec copy {MERGED_MP4_PATH}")
os.remove(MERGED_TS_PATH)
