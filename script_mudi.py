# 
# 
# mudi stands for "music director", helps me to manage my music collection
# 
# 
# 
# 


import csv

fieldnames = ['id', 'tags', 'title'] # tags are split by a '|'. i.e. "dance|popping|cool", "dance,party|rock|afro"
# with open('my_music.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()

def downloadPlaylist(url: str, dictionary: str):
    from script_ytdlp import infoOf, fieldId, fieldTitle, fieldPlaylistTitle
    from re import match
    snapshot = infoOf(url, f'{fieldId},{fieldPlaylistTitle},[{fieldTitle}]').split('\n')
    pattern = r'([\w-]{11}),(.+),\[(.+)\]'
    
    with open(dictionary, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in snapshot:
            matching = match(pattern, item)
            id = matching.group(1)
            tags = matching.group(2)
            title = matching.group(3)
            writer.writerow([id, tags, title])

    from script_ytdlp import download, fieldId
    from book import mp3
    download(url, mp3, f'repo/{fieldId}')
    

# TODO: finally mix rows with same id


# 
# 
# TODO: in python, only get 2025 dancing music
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