import subprocess
import os

print(
    '\n'
    '-----------------------------------------------\n'
    'yt-dlp.py helps downloading vedio by terminal.\n'
    "It's an implementation for https://github.com/yt-dlp/yt-dlp \n"
    "Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md \n"
    '-----------------------------------------------\n'
)

embedThmbnail: str = '--embed-thumbnail'
yesPlaylist: str = '--yes-playlist'

output: str = '-o'
outputFileNameFormat: str = f'%(title)s'

# see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection-examples
extractAudio: str = '-x'
formatAudio: str = '--audio-format'
formatVideo: str = '-f'
supportedAudioFormat = ['best', 'aac', 'alac', 'flac', 'm4a', 'mp3', 'opus', 'vorbis', 'wav'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#post-processing-options
supportedVideoFormat = ['avi', 'flv', 'mkv', 'mov', 'mp4', 'webm'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#video-format-options


def findLocation() -> str:
    def availableDirs() -> str:
        return next(os.walk('.'))[1]

    while (True):
        location = input(f'file location (default: {os.getcwd()}): ')

        args = location.split()
        argsLength = len(args)
        if argsLength == 0:
            return outputFileNameFormat
        
        if argsLength == 1:
            return f'{args[0]}/{outputFileNameFormat}'
        
        if argsLength == 2:
            command = args[0]
            location = args[1]

            if command == 'cd':
                try:
                    os.chdir(location)
                    print(f'availables dirs: {availableDirs()}')
                    continue
                except FileNotFoundError:
                    print(
                        f'directory not found: {location},\n'
                        f'availables: {availableDirs()}\n'
                    )
        
        print(
            f"unknown command: {args}\n"
            "USAGES:\n"
            "\t1. press enter to ensure the default location\n"
            "\t2. 'cd /your_path', pending to provide a location\n"
        )

def findFormat() -> str:
    while (True):
        format = input('vedio format (default: mp3): ')
        format = 'mp3' if format == '' else format

        if format in supportedAudioFormat:
            return [extractAudio, formatAudio, format]
        elif format in supportedVideoFormat:
            requireBestVedio = input('require best vedio (Y/N): ').capitalize()
            if requireBestVedio == 'Y':
                format = f'bv*[ext={format}]+ba[ext=m4a]'
            else:
                print(f'except Y/y or N/n: {requireBestVedio}')
                continue
            
            return [formatVideo, format]
        
        print(
            f"unknown command: {format}\n"
            "USAGES:\n"
            f"\t1. press enter to ensure the default format\n"
            f"\t2. input an audio format of {supportedAudioFormat}\n"
            f"\t3. input a vedio format of {supportedVideoFormat}\n"
        )


class YoutubeDownloader:
    commands = ['yt-dlp']
    def __init__(this, url: str):
        this.commands.append(embedThmbnail)

        # location, format
        this.commands.extend([output, findLocation()])
        this.commands.extend(findFormat())
        
        this.commands.append(url)

        
        subprocess.call(this.commands)
    

YoutubeDownloader(url=input('url: '))

