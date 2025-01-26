import os
from subprocess import call

# 
# 
# 
# lambdas
# 
# 
# 
pathSplittext = lambda source: os.path.splitext(source)
pathAbspath = lambda source: os.path.abspath(source)
getCwd = lambda : os.getcwd()
getCwdDirectories = lambda : walking('.')[1]
getCwdFiles = lambda : walking('.')[2]
walking = lambda location: next(os.walk(location))

# _sibling = lambda file: os.path.join(os.path.dirname(__file__), file)

#
#
#
# functions
#
# 
# 
def foreachFiles(consume, parent: str = '', includeSub: bool = False):
    children = walking(parent if parent else '.')

    print(f'iterating on {getCwd()} ...')
    [consume(os.path.join(parent, child)) for child in children[2]]
    
    if includeSub:
        def nesting(subDirs: list, p: str):
            for subDir in subDirs:
                os.chdir(subDir)
                children = walking('.')
                p = os.path.join(p, subDir)

                if children[1]:
                    nesting(children[1], p)

                if children[2]:
                    print(f'calculating for /{p} ...')
                    [consume(os.path.join(parent, p, child)) for child in children[2]]
                
                os.chdir('..')
        nesting(children[1], '')


def chdirAndShow(location: str, successShow: bool = False) -> bool: # return true when choosen
    try:
        os.chdir(location)
        if successShow: call(['ls', '-d']) # list only directories
        return True
    except FileNotFoundError:
        print(f'location not found: {location}')
        print('available directories'.center(20, '-'))
        call(['ls', '-d'])
        return False

def raiseInvalidUsecase(apiName: str, option: str, supportedUsecases: list):
    raise Exception(
        f'invalid usecase: {option},\n'
        f'availables: {supportedUsecases}\n'
        f'from: {apiName}'
    )

# 
# 
# 
def removerCareful(match, pattern: str):
    from script_input import ensureYorN
    from script_os import pathAbspath
    def checking(source: str):
        if match(pattern, source):
            if ensureYorN(f'sure to remove {pathAbspath(source)}?', emptyEqualY=True):
                os.remove(source)

    return checking

def removeAllFileOfPattern(pattern: str, includeSub: bool, check: bool):
    from script_os import foreachFiles
    from re import match
    remover = lambda source: source
    if check:
        remover = removerCareful(match, pattern)
    else:
        remover = lambda source: os.remove(source) if match(pattern, source) else None

    foreachFiles(remover, includeSub=includeSub)


# 
# 
# 
# functions ---- readyTo...
# 
# 
# 
def readyToRemoveFileOfPattern(check: bool = True):
    from script_input import ensureNotEmpty
    pattern = ensureNotEmpty('pattern: ')
    removeAllFileOfPattern(pattern, includeSub=False, check=check)