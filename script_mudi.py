# 
# 
# mudi stands for "music director", helps me to manage my music collection
# 
# 
# 

file_dictionary = 'my_music_dictionary.csv'
file_location = '/Users/nomisal/Downloads/music'
# file_parent = 'repo'
file_parent = 'test'

from script_ytdlp import fieldId, fieldTitle, fieldPlaylistTitle
encoding = 'utf-8'
formatInfoString = f'{fieldId},{fieldPlaylistTitle},[{fieldTitle}]' # playlist title as tags
formatCsvField = ['id', 'tags', 'title'] 
formatFile = f'{file_parent}/{fieldId}'
# with open('my_music.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=formatCsvField)
#     writer.writeheader()

def hasPermission():
    from os import chdir, path
    chdir(file_location)
    print(f'now in {file_location}...\n')
    if not path.isfile(file_dictionary):
        print(f'require {file_dictionary} in {file_location}')
        return False
    return True

def appendCsvThenDownloadPlaylist(url: str):
    from script_ytdlp import infoOf, download
    appendCsv(infoOf(url, formatInfoString,
        # needsCookie=True
    ).split('\n'))
    
    from book import mp3
    download(url, mp3, formatFile,
        # needsCookie=True
    )
    

def appendCsv(snapshot: str):
    print(f'append on {file_dictionary}...')
    with open(file_dictionary, 'a', newline='', encoding=encoding) as file:
        from csv import writer
        from re import match
        w = writer(file)
        pattern = r'([\w-]{11}),(.+),\[(.+)\]'
        for item in snapshot:
            print(item)
            matching = match(pattern, item)
            if matching:
                id = matching.group(1)
                tags = matching.group(2)
                title = matching.group(3)
                w.writerow([id, tags, title])
    
    print('finished\n')

def readCsvForTitle(id: str):
    with open(file_dictionary, 'r', encoding=encoding) as file:
        from csv import reader
        r = reader(file)
        next(r)
        for item in r:
            if item[0] == id: return item[2]

    raise Exception(f'{id}.mp3 not found in {file_location}/repo')

def copyMusicTo(source: str, path: str):
    import os
    if not os.path.exists(path): os.mkdir(path)
    from shutil import copy2
    from script_ import nameFromPath
    copy2(source, f'{path}/{readCsvForTitle(nameFromPath(source))}.mp3')


# 
# in python, only get 2025 dancing music
# TODO: exluding tags to caculate then export audio
# 


# TODO: in flutter,
# - basic audio set management
#   - demo entire audio set (id, title, tags)
#   - demo partial audio set after filter by name, tag(s)
#   - know the tags of an audio, some audio
# - advance tag management
#   - filter tags by tag (parent/children, super/sub)
#   - rename tag
#   - visualize all the tags and their relationships
#   - recommand removing weak tag (only some music)
# - iterating function
#   - iterate untagged playlist, tagged playlist
#   - be able to listen to the current music, preview and go to previous or next item
#   - updating tag when iterating
# 