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


def download_video(chunklist_url: str, title: str) -> None:
    MERGED_TS_PATH = os.path.join(DATA_DIR, f"{title}-merged.ts")
    MERGED_MP4_PATH = os.path.join(DATA_DIR, f"{title}.mp4")

    if os.path.isfile(MERGED_MP4_PATH):
        print(f"🟢 {title}.mp4 already exists")
        return
    else:
        print(f"🟡 downloading {title}.mp4")

    # download the chunklist
    print(f"downloading chunklist")
    chunklist_path = os.path.join(DATA_DIR, chunklist_url.split("/")[-1])
    os.system(f"wget --quiet {chunklist_url} -P {DATA_DIR}")
    with open(chunklist_path) as f:
        chunklist = f.read()
    os.remove(chunklist_path)

    # download all ts files
    print(f"grouping chunks")
    base_url = "/".join(chunklist_url.split("/")[:-1])
    file_pattern = re.compile("[^\n].*_\d+\.ts")
    files = re.findall(file_pattern, chunklist)
    file_count = len(files)
    chunks = []
    for i in range(10):
        start_i = round(i * file_count / 10)
        end_i = min(round((i + 1) * file_count / 10), file_count)
        chunks.append([f"{base_url}/{f}" for f in files[start_i:end_i]])
    assert sum([len(c) for c in chunks]) == file_count

    # download all ts files
    print(f"downloading chunks")
    for i, c in enumerate(chunks):
        os.system("wget --quiet " + " ".join(c) + f" -P {RAW_DATA_DIR}")
        print(f"{(i+1) * 10}% done")

    # merge all ts files into one ts file + delete individual ts files
    print(f"merging ts chunks")
    raw_ts_files = [os.path.join(RAW_DATA_DIR, f) for f in files]
    os.system(f"cat " + " ".join(raw_ts_files) + f" > {MERGED_TS_PATH}")
    shutil.rmtree(RAW_DATA_DIR)

    # convert the merged ts file into an mp4 file + delete merged ts file
    print(f"converting into mp4")
    if os.path.isfile(MERGED_MP4_PATH):
        os.remove(MERGED_MP4_PATH)
    os.system(
        f"ffmpeg -loglevel error -i {MERGED_TS_PATH} -acodec copy -vcodec copy {MERGED_MP4_PATH}"
    )
    os.remove(MERGED_TS_PATH)
    print(f"🟢 finished {title}.mp4")


if __name__ == "__main__":
    download_video(CONFIG["chunklist_url"], CONFIG["title"])
