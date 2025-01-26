# 
# 
# 
# 
# 
# 
def inputOrDefault(title: str, option):
    value = input(f'{title} (default: {option}): ')
    return value if value else option

def inputOrDefaultIfEmpty(title: str, option, value):
    if value: return value
    return inputOrDefault(title, option)

def ensureNotEmpty(message: str) -> str:
    while True:
        value = input(message)
        if value: return value

def ensureValidFile(title: str):
    from script_os import getCwdFiles
    availableFiles = getCwdFiles()
    while True:
        file = ensureNotEmpty(title)
        if file in availableFiles: return file
        print(f'file not found: {file}')

def ensureValidUrl(title: str = 'url: '):
    from validators import url as validate
    while True:
        url = ensureNotEmpty(title)
        if validate(url): return url
        print(f'invalid url: {url}')

def ensureYorN(question: str, emptyEqualY: bool = False) -> bool:
    while True:
        code = input(question + f" (y/n{', default: y' if emptyEqualY else ''}): ").upper()
        if emptyEqualY and not code: return True
        if code == 'Y': return True
        if code == 'N': return False

def ensureValidOption(options: dict) -> list:
    names = list(options.keys())
    print('available options:\n')
    print('\n'.join(
        ['\t' + f'{i+1}'.ljust(7, '-') + f' {name}' for i, name in enumerate(names)]
    ))
    print()

    while True:
        try:
             name = names[int(ensureNotEmpty('your option: '))-1]
             return (name, options[name])
        except TypeError or IndexError  : print(f'require integer 1~{len(options)}')
        except Exception as e           : raise e


def ensureLocation() -> str:
    from script_os import getCwd, chdirAndShow
    while True:
        cwd = getCwd()
        destination = input(f'location (default: {cwd}): ')
        if not destination: return cwd
        chdirAndShow(destination, True)
