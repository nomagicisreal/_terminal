import os.path as path
import os

# 
# 
# 
# lambdas
# 
# 
# 
osSibling = lambda file: path.join(path.dirname(__file__), file)
osWalking = lambda location: next(os.walk(location))
osCwds = lambda : osWalking('.')[0]
osCwdFiles = lambda : osWalking('.')[1]

#
#
#
# functions
#
# 
# 
def foreachFiles(consume, parent: str = '', includeSub: bool = False):
    children = osWalking(parent if parent else '.')

    print(f'iterating on {os.getcwd()} ...')
    [consume(path.join(parent, child)) for child in children[2]]
    
    if not includeSub:
        return
    def nesting(subDirs: list, p: str = ''):
        for subDir in subDirs:
            os.chdir(subDir)
            children = osWalking('.')
            p = path.join(p, subDir)

            if children[1]:
                nesting(children[1], p)

            if children[2]:
                print(f'calculating for /{p} ...')
                [consume(path.join(parent, p, child)) for child in children[2]]
            
            os.chdir('..')
    nesting(children[1])

def travelOnDir(location: str) -> bool: # return true when choosen
    try:
        os.chdir(location)
        print(f'available directories: {osCwds()}')
        return True
    except FileNotFoundError:
        print(
            f'directory not found: {location},\n'
            f'availables: {osCwds()}\n'
        )
        return False

def raiseUnimplementUsecase(script: str, usecase: str):
    raise Exception(f'Unimplement "{usecase}" for "{script}"')

    
def ensuringCwd():
    from script_input import whileEnsureLocation
    whileEnsureLocation(os.getcwd(), travelOn=travelOnDir)
