import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

print("1. Video Download")
print("2. Audio (MP3) Download")

choice = input("Option select করো: ")
url = input("Video URL দাও: ")

if choice == '1':
    download_video(url)
elif choice == '2':
    download_audio(url)
else:
    print("Invalid option!")
