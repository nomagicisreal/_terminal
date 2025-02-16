# 
# 
# mudi stands for "music director", helps me to manage my music collection
# 
# 
# 

file_dictionary = 'my_music_dictionary.csv'
file_location = '/Users/nomisal/Downloads/music'
file_parent = 'repo'
# file_parent = 'test'

from script_ytdlp import fieldId, fieldTitle, fieldPlaylistTitle
encoding = 'utf-8'
formatInfoString = f'{fieldId},{fieldPlaylistTitle},[{fieldTitle}]' # playlist title as tags
formatCsvField = ['id', 'tags', 'title'] 
formatFile = f'{file_parent}/{fieldId}'
# with open('my_music.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=formatCsvField)
#     writer.writeheader()

def passPermission():
    from os import chdir, path
    chdir(file_location)
    print(f'now in {file_location}...\n')
    if not path.isfile(file_dictionary):
        print(f'require {file_dictionary} in {file_location}')
        return False
    return True

# 
# 
# 
# append csv
# 
# 
# 
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

# 
# 
# 
# read csv
# 
# 
# 
def searchCsv(id: str = '', tagsSet: list = []):
    if id and tagsSet:
        raise Exception(
            'you must provide only id or only tags\n'
            f'instead, you both provide id({id}) and tags({tagsSet})'
        )
    if not id and not tagsSet:
        raise Exception('you must provide id or tags to read for title')
    
    with open(file_dictionary, 'r', encoding=encoding) as file:
        from csv import reader
        row = reader(file)
        next(row)

        # return only title
        if id:
            for item in row:
                if item[0] == id: return item[2]
            print(f'no music with id({id}) in {file_dictionary}')
        
        # return rows with tags
        if tagsSet:
            items = []
            for item in row:
                for tags in tagsSet:
                    if tags == item[1]:
                        items.append(item)
                        continue
            return items

def demoTagsSet(tagsSet: list, description: str = 'all'):
    if not tagsSet: print('the tagsSet is empty')
    from script_ import printDevider
    printDevider(f'{description} tags')
    print('\n'.join(tagsSet))
    printDevider(f'{description} tags')

def demoAndGetTagsSet():
    tagsSet = []
    with open(file_dictionary, 'r', encoding=encoding) as file:
        from csv import reader
        r = reader(file)
        next(r)
        for item in r:
            tags = item[1]
            if tags in tagsSet: continue
            tagsSet.append(tags)
    
    tagsSet.sort()
    demoTagsSet(tagsSet)
    return tagsSet

def filterTags():
    remain = demoAndGetTagsSet()
    excluded = []
    print('USAGE:')
    print('1. leave empty and press enter to keep the current tags set as the result')
    print('2. input a pattern to remove all tags containing it')
    print("3. input patterns connected by ',' to remove all tags containing one of them")

    def filter(pattern, remain: list, excluded: list):
        result = remain.copy()
        for tags in remain:
            if pattern in tags:
                print(f'remove tags: {tags}')
                result.remove(tags)
                excluded.append(tags)
        if len(remain) == len(result): return False
        remain.clear()
        remain.extend(result)
        return True

    while True:
        pattern: str = input('\ntags pattern: ')
        if not pattern: return remain
        patternList = pattern.split(',')
        removeSomething = False
        for pattern in patternList:
            removeAnything = filter(pattern, remain, excluded)
            if removeAnything:
                removeSomething = True
                continue
            print(f"there is no tags contain '{pattern}'")

        if removeSomething:
            demoTagsSet(remain, 'remain')
            print(f"\nremoved tags: {','.join(excluded)}")


# 
# 
# 
# 
# overall
# 
# 
# 
# 
def copyMusicTo(source: str, path: str):
    import os
    import os.path as p
    if not p.exists(path): os.mkdir(path)
    from shutil import copy2
    from script_ import nameFromPath
    copy2(
        source,
        p.join(path, f'{searchCsv(id=nameFromPath(source))}.mp3'.replace('/', '|'))
    )

def copyMusicToByTags(path: str):
    import os
    import os.path as p
    if not p.exists(path): os.mkdir(path)
    tagsSet = filterTags()
    from script_ import printDevider
    printDevider(f'get tags set: {tagsSet}')
    items = searchCsv(tagsSet=tagsSet)
    printDevider(f'found items in {file_dictionary}')
    for item in items: print(','.join(item))
    print('copy on process...\n')

    from shutil import copy2
    for item in items:
        parent = p.join(path, item[1])
        if not p.exists(parent): os.mkdir(parent)
        copy2(
            p.join(file_parent, f'{item[0]}.mp3'),
            p.join(parent, f'{item[2]}.mp3'.replace('/', '|')),
        )

    print('copy finished!')


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