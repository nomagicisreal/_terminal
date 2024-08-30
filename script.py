import os.path as path
import os
import subprocess

# 
# 
# 
# lambdas
# 
# 
# 
osPathRealParent = lambda name: path.dirname(path.realpath(name))
osPathRealSibling = lambda one, another: path.join(osPathRealParent(one), another)
osPathBasename = lambda name: path.basename(name)
osPathSplitext = lambda name: path.splitext(name)
osPathName = lambda name: path.splitext(name)[0]
osPathExtension = lambda name: path.splitext(name)[1][1:]

cwdChildren = lambda : next(os.walk('.'))
cwdDirectories = lambda : cwdChildren()[0]
cwdFiles = lambda : cwdChildren()[1]

askForLocation = lambda : input(f'location (default: {os.getcwd()}): ')
askForLocationInstruction = lambda arg : print(
    f"unknown command: {arg}\n"
    "USAGES:\n"
    "\t1. press enter to ensure the default location\n"
    "\t2. 'cd /your_path', pending to provide a location\n"
)

#
#
#
# functions
#
# 
# 
def foreachFiles(consume, includeSub: bool = True):
    children = cwdChildren()

    print(f'calculating for location ...')
    [consume(child) for child in children[2]]
    
    if not includeSub:
        return

    def nesting(subDirs: list, parent: str = ''):
        for subDir in subDirs:
            os.chdir(subDir)
            children = cwdChildren()
            p = path.join(parent, subDir)

            if children[1]:
                nesting(children[1], p)

            if children[2]:
                print(f'calculating for /{p} ...')
                [consume(child) for child in children[2]]
            
            os.chdir('..')
    
    nesting(children[1])

def chooseDirectoryOn(location: str) -> bool: # return true when choosen
    try:
        os.chdir(location)
        print(f'available directories: {cwdDirectories()}')
        return True
    except FileNotFoundError:
        print(
            f'directory not found: {location},\n'
            f'availables: {cwdDirectories()}\n'
        )
        return False

def raiseUnimplementUsecase(script: str, usecase: str):
    raise Exception(f'Unimplement "{usecase}" for "{script}"')

# 
# 
# function ... terminal interface
# 
# 
def whileInputYorN(question: str) -> bool:
    while True:
        code = input(f'{question} (y/n): ').capitalize()
        if not code: continue
        if code == 'Y': return True
        if code == 'N': return False
        raise Exception('pleas input Y or N')

def whileInputUrl() -> str:
    while True:
        url = input('url: ')
        if url: return url

def whileInputValidOption(options: dict) -> list:
    optionNames = list(options.keys())
    print(
        f'available options--\n' +
        ''.join([f'\t\t \\--{i+1}-- {name}\n' for i, name in enumerate(optionNames)])
    )
    while True:
        o: str = input('your option: ')
        if not o: continue
        errorMessage: str = f'\nno such option: {o}\n'

        try:
             name = optionNames[int(o)-1]
             return [options[name], name]
        except TypeError:       errorMessage += f'please input integer instead of {o}'
        except IndexError:      errorMessage += f'require 0 < {o} < {len(options)})'
        except Exception as e:  errorMessage = e
        print(errorMessage)
    