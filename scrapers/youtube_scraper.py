import os
from googleapiclient.discovery import build


def fetch_youtube_comments(video_url, max_comments=500, api_key=None):
    """
    Fetch comments from a YouTube video.
    Args:
        video_url (str): Full YouTube video URL.
        max_comments (int): Max number of comments to fetch.
    Returns:
        List of comment texts (strings).
    """
    # Extract video ID from URL
    
    video_id = None
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]

    print(f"Extracted video ID: {video_id}")  # DEBUG

    if not video_id:
        return []


    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )
        response = request.execute()

        while response and len(comments) < max_comments:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
                if len(comments) >= max_comments:
                    break
            if 'nextPageToken' in response and len(comments) < max_comments:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    textFormat="plainText",
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
            else:
                break
    except Exception as e:
        print("YouTube API error:", e)
    
    return comments
