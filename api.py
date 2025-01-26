

def main():
    import api_os
    import api_ytdlp
    import api_ffmpeg

    from script_input import ensureValidOption
    option = ensureValidOption({
        **{usecase : api_os.processing for usecase in api_os.usecases},
        **{usecase : api_ytdlp.processing for usecase in api_ytdlp.usecases},
        **{usecase : api_ffmpeg.processing for usecase in api_ffmpeg.usecases},
    })
    option[1](option[0])

main()
print()