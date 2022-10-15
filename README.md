# Video Transport Stream Downloader

## 📦 What does it do?

This tool exports an MP4 video file from a `.m3u8` chunklist file on the internet. These files contain a list of `.ts` file names which each contain a short video snippet. Example:

```m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:8.333,
media_some_video_id_0.ts
#EXTINF:8.334,
media_some_video_id_1.ts
#EXTINF:8.333,
media_some_video_id_2.ts
...
```

After fetching the chunklist, the tool will download all `.ts` files, merge them into one big file and convert this file into an MP4 file. It uses `curl`, `wget` and `ffmpeg` under the hood.

# ⚔️ How to use it?

1. Install python3 (https://www.python.org/)
2. Install ffmpeg (https://ffmpeg.org/)
3. Make sure the `curl`, `wget` and `cat` command work on your system
4. Use `config.default.json` to create a `config.json` file in the project directory
5. Run `python3 main.py`

🎁 Your output file can be found at `out/<config.title>.mp4`.
