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
    wget_call_exit_code = os.system(f"wget --quiet {chunklist_url} -P {DATA_DIR}")
    if wget_call_exit_code != 0:
        print(f"🔴 wget download of chunklist failed")
        return
    with open(chunklist_path) as f:
        chunklist = f.read()
    os.remove(chunklist_path)

    # download all ts files
    print(f"grouping chunks")
    base_url = "/".join(chunklist_url.split("/")[:-1])
    file_pattern = re.compile("[^\n].*\.ts")
    raw_file_list = list(sorted(re.findall(file_pattern, chunklist)))
    file_urls = [
        (f if f.startswith("http") else f"{base_url}/{f}") for f in raw_file_list
    ]
    file_names = list(sorted([f.split("/")[-1] for f in raw_file_list]))
    file_count = len(file_names)
    url_chunks = []
    for i in range(10):
        start_i = round(i * file_count / 10)
        end_i = min(round((i + 1) * file_count / 10), file_count)
        url_chunks.append(file_urls[start_i:end_i])
    assert sum([len(c) for c in url_chunks]) == file_count

    # download all ts files
    print(f"downloading chunks")
    for i, c in enumerate(url_chunks):
        wget_call_exit_code = os.system(
            "wget --quiet " + " ".join(c) + f" -P {RAW_DATA_DIR}"
        )
        if wget_call_exit_code != 0:
            print(f"🔴 wget download of video snippets failed")
            return
        print(f"{(i+1) * 10}% done")

    # merge all ts files into one ts file + delete individual ts files
    print(f"merging ts chunks")
    raw_ts_files = [os.path.join(RAW_DATA_DIR, f) for f in file_names]
    os.system(f"cat " + " ".join(raw_ts_files) + f" > {MERGED_TS_PATH}")
    shutil.rmtree(RAW_DATA_DIR)

    # convert the merged ts file into an mp4 file + delete merged ts file
    print(f"converting into mp4")
    if os.path.isfile(MERGED_MP4_PATH):
        os.remove(MERGED_MP4_PATH)
    ffmpeg_call_exit_code = os.system(
        f"ffmpeg -loglevel error -i {MERGED_TS_PATH} -acodec copy -vcodec copy {MERGED_MP4_PATH}"
    )
    if ffmpeg_call_exit_code == 0:
        os.remove(MERGED_TS_PATH)
        print(f"🟢 finished {title}.mp4")
    else:
        print(f"🔴 ffmpeg failed")


if __name__ == "__main__":
    for v in CONFIG["videos"]:
        download_video(v["chunklist_url"], v["title"])
