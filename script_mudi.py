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
formatInfoString = f'{fieldId},,[{fieldTitle}]'
formatInfoStringForPlaylist = f'{fieldId},{fieldPlaylistTitle},[{fieldTitle}]'
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
def appendCsvThenDownload(url: str, requirePlaylist: bool):
    from script_ytdlp import infoOf, download, isYoutubeVideoUrlWithPlaylist
    urlContainPlaylist = isYoutubeVideoUrlWithPlaylist(url)
    info = ''
    if requirePlaylist:
        if not urlContainPlaylist:
            raise Exception(
                'require youtube url containing playlist id\n' +
                'format 1: https://www.youtube.com/playlist?list=...\n' + 
                'format 2: https://www.youtube.com/watch?v=...&list=...&index=...'
            )
        info = infoOf(url, formatInfoStringForPlaylist,
            # needsCookie=True
        ).split('\n')
        
    else:
        if urlContainPlaylist:
            raise Exception(
                'require youtube url continaing only video id\n' +
                'invalid format 1: https://www.youtube.com/playlist?list=...\n' + 
                'invalid format 2: https://www.youtube.com/watch?v=...&list=...&index=...'
            )

        from counter import whileInputNotEmpty
        info = [infoOf(url, formatInfoString,
            # needsCookie=True
        ).replace(',,[', f",{whileInputNotEmpty('tags for audio: ').strip()},[")]

    appendCsv(info)
    from book import mp3
    download(url, mp3, formatFile,
        # needsCookie=True
    )
    

def appendCsv(snapshot: list):
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
                if item[0] == id:
                    print(f'finding items in {file_dictionary}')
                    return item[2]
            print(f'no music with id({id}) in {file_dictionary}')
        
        # return rows with tags
        if tagsSet:
            items = []
            for item in row:
                for tags in tagsSet:
                    if tags == item[1]:
                        items.append(item)
                        continue
            from script_ import demoItems
            demoItems(
                [','.join(item) for item in items],
                messageNoItem=f'there is no music found in {file_dictionary} with any tag in {tagsSet}',
                dividerTitle=f'found items in {file_dictionary}'
            )
            return items

def getTagsSetSorted():
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
    return tagsSet

def filterTags(inclusive: bool, whileInputNotEmpty, whileInputReject):
    verb = 'include' if inclusive else 'exclude'
    print(
        '\nUSAGE:\n' +
        f'1. input a pattern to {verb} all tags containing it\n' +
        f"2. input patterns connected by ',' to {verb} all tags containing one of them\n"
    )
    remain = getTagsSetSorted()
    target = []

    def filter(pattern, remain: list, target: list):
        result = remain.copy()
        for tags in remain:
            if pattern in tags:
                result.remove(tags)
                target.append(tags)
        if len(remain) == len(result): return False
        remain.clear()
        remain.extend(result)
        return True

    print(f'overall tags: {remain}\n')
    values = (lambda: target) if inclusive else (lambda: remain)
    dividerTitle = 'included tags' if inclusive else 'remain tags'
    from script_ import demoItems
    while True:
        pattern: str = whileInputNotEmpty('tags pattern: ')
        patternList = pattern.split(',')
        matchSomething = False
        for pattern in patternList:
            matchAnything = filter(pattern, remain, target)
            if matchAnything:
                matchSomething = True
                continue
            print(f"there is no tags contain '{pattern}'\n{remain=}")

        if matchSomething: demoItems(values(), dividerTitle)
        if whileInputReject('\ncontinue selecting tags?'):
            result = values()
            if not result:
                print("you're not select any tags, please select some tags")
                continue
            print(f'selected tags: {result}')
            return result

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
    os.makedirs(path, exist_ok=True)

    import os.path as p
    from shutil import copy2
    from script_ import nameFromPath
    copy2(
        source,
        p.join(path, f'{searchCsv(id=nameFromPath(source))}.mp3'.replace('/', '|'))
    )

def copyMusicToByTags(path: str, whileInputNotEmpty, whileInputReject, inclusive: bool):
    import os
    os.makedirs(path, exist_ok=True)
    tagsSet = filterTags(inclusive, whileInputNotEmpty, whileInputReject)
    items = searchCsv(tagsSet=tagsSet)

    print('copy on process...')
    import os.path as p
    from shutil import copy2
    for item in items:
        parent = p.join(path, item[1])
        if not p.exists(parent): os.mkdir(parent)
        copy2(
            p.join(file_parent, f'{item[0]}.mp3'),
            p.join(parent, f'{item[2]}.mp3'.replace('/', '|')),
        )
    print('copy finished!\n')


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