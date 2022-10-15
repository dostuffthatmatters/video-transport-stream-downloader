import os

SRC = "https://.../some.m3u8"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKLIST_PATH = os.path.join(PROJECT_DIR, "out", "chunklist.m3u8")

os.system(f"curl {SRC} > {CHUNKLIST_PATH}")

with open(CHUNKLIST_PATH) as f:
    chunklist = f.read()
