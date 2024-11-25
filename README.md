# ytdl-nfo

A tool to download YouTube videos with thumbnails and generate a metadata `.nfo` file for media servers.
Ideal for Jellyfin / Emby users + archivists.

## Features
- Downloads videos with subtitles, thumbnails, and `.nfo` metadata.
- Auto-saves in a folder named after the video in working directory by default.
- Ability to specify alternate directory with `--output_directory`

## Installation
Make sure pip is up to date:
```bash
pip install --upgrade pip
```
Install:
```bash
git clone https://github.com/htmlgxn/ytdl-nfo.git
cd ytdl-nfo
pip install .
```

## Usage
To download in working directory (creates a subfolder):
```bash
ytdl-nfo <youtube-url>
```
To specify alternate directory:
```bash
ytdl-nfo <youtube-url> --output_directory /path/to/directory
```

## Optional Settings
With heavy usage, YouTube may block your requests with this something along the lines of this error:
```bash
ERROR: [youtube] <video_id>: Sign in to confirm you’re not a bot. This helps protect our community. Learn more
```
To fix this, use [Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) or something similar. Export from a tab with https://youtube.com/* opened to a txt file (Export as / cookies.txt) to the parent ytdl_nfo folder, and uncomment this in the src/ytdl_nfo/ytdl_nfo.py file:
```bash
#'cookiefile': '../../cookies.txt',
```

Another optional setting is to set a rate limit if YouTube is giving you a really hard time. Uncomment / edit this line in the src/ytdl_nfo/ytdl_nfo.py file (default is 1 MB / sec):
```bash
#'ratelimit': 1000000,
```