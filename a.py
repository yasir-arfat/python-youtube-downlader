from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

def download_video(url, save_path):
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        stream.download(save_path)
        
        print(f"Video downloaded successfully to {save_path}")
    except VideoUnavailable:
        print("The video is unavailable. Please check the URL.")
    except RegexMatchError:
        print("The video URL format is incorrect.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=B7obgkddqdk"  # Replace with your desired YouTube video URL
save_directory = "C:/Users/a/Desktop"  # Replace with your desired save directory
download_video(video_url, save_directory)


