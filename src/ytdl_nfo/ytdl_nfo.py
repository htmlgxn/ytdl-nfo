import os
import re
from pathlib import Path
from yt_dlp import YoutubeDL
import argparse

def sanitize_filename(name):
    # Convert to lowercase and replace spaces with dashes
    name = name.lower().replace(' ', '-')
    # Remove or replace unwanted characters
    name = re.sub(r'[.\'()<>"\\|?*]|[^-\w]', '', name)
    return name

def get_metadata(video_url):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            return info_dict
        except Exception as e:
            print(f"Error occurred while fetching metadata for {video_url}: {e}")
            return None

def download_video(video_url, output_template, output_directory, filename):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Force .mp4 container
        'merge_output_format': 'mp4',  # Ensure output is .mp4
        'writesubtitles': True,        # Download subtitles
        'subtitlesformat': 'vtt',      # Preferred subtitle format for download
        'convertsubtitles': 'srt',     # Convert subtitles to .srt
        'subtitleslangs': ['all'],     # All languages
        'writethumbnail': True,        # Download thumbnail
        'postprocessors': [
            {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'},  # Convert thumbnail to .jpg
        ],
        'outtmpl': {
            'default': output_template,
            'subtitle': str(output_directory / f"{filename}.%(subtitle_lang)s.%(ext)s"), # Save subtitles with the same filename
            'thumbnail': str(output_directory / f"{filename}.%(ext)s"),  # Save thumbnail with the same filename
        },
        # Add a cookie file from an extension (e.g. Get cookies.txt) if you are getting Sign In errors from YouTube
        #'cookiefile': '../../cookies.txt',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        },
        # Uncomment if you want to set a rate limit / YouTube is giving you a hard time (1 MB/s)
        #'ratelimit': 1000000,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            print(f"Downloaded: {output_template}")
        except Exception as e:
            print(f"Error occurred while downloading video {video_url}: {e}")

def create_nfo_file(metadata, nfo_path):
    title = metadata.get("title", "Unknown Title")
    channel = metadata.get("uploader", "Unknown Channel")
    video_id = metadata.get("id", "Unknown Video ID")
    upload_date = metadata.get("upload_date", "")
    formatted_date = (
        f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        if upload_date
        else "Unknown Date"
    )
    upload_year = (
        f"{upload_date[:4]}"
        if upload_date
        else "Unknown Year"
    )
    description = metadata.get("description", "Unknown Description")
    nfo_content = f"""<episodedetails>
  <title>{title}</title>
  <id>{video_id}</id>
  <studio>{channel}</studio>
  <releasedate>{formatted_date}</releasedate>
  <year>{upload_year}</year>
  <plot>{description}</plot>
</episodedetails>
"""
    try:
        with open(nfo_path, "w", encoding="utf-8") as nfo_file:
            nfo_file.write(nfo_content)
        print(f".nfo file created: {nfo_path.name}")
    except IOError as e:
        print(f"Error writing .nfo file {nfo_path}: {e}")

def download_video_and_create_nfo(video_url, output_directory=None):
    metadata = get_metadata(video_url)
    if metadata is None:
        return

    title = metadata.get("title", "unknown-title")
    channel = metadata.get("uploader", "unknown-channel")

    safe_title = sanitize_filename(title)
    safe_channel = sanitize_filename(channel)
    filename = f"{safe_title}_{safe_channel}"

    # If no output directory is provided, create a folder with the filename in the working directory
    if output_directory is None:
        output_directory = Path.cwd() / filename
    else:
        output_directory = Path(output_directory)

    output_directory.mkdir(parents=True, exist_ok=True)

    # Output template with dynamic extension
    output_template = str(output_directory / f"{filename}.%(ext)s")

    download_video(video_url, output_template, output_directory, filename)

    # Assuming the video file has .mp4 extension
    video_file = output_directory / f"{filename}.mp4"
    if video_file.exists():
        nfo_path = video_file.with_suffix('.nfo')
        create_nfo_file(metadata, nfo_path)
    else:
        print(f"Downloaded video file not found for {video_url}.")

def main():
    parser = argparse.ArgumentParser(description='Download video and create .nfo file.')
    parser.add_argument('video_url', help='URL of the video to download')
    parser.add_argument('-d, --dir', help='Directory to save the video and .nfo file (optional)')
    args = parser.parse_args()

    download_video_and_create_nfo(args.video_url, args.dir)
