# ytdl-nfo

A tool to download YouTube videos - with thumbnails and generate `.nfo` file for media server.
Ideal for Jellyfin / Emby users.

## Features
- Downloads videos with subtitles, thumbnails, and `.nfo` metadata.
- Auto-saves in a folder named after the video by default.

## Installation
Make sure pip is up to date.
```bash
git clone https://github.com/htmlgxn/ytdl-nfo.git
cd ytdl-nfo
pip install .
```

## Usage
To download in working directory (creates a subfolder)
```bash
ytdl-nfo <youtube-url>
```
To change from default directory
```bash
ytdl-nfo <youtube-url> --output_directory /path/to/directory
```
