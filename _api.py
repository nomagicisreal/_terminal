import subprocess
from api import *

def argumentOf(argv: list) -> list:
    fileName: str = argv[0]
    names = fileName.split('.')
    assert(len(names) == 2, f'unknown file: {fileName}')
    return [
        findCommand(names[1]),
        findPath(fileName)
    ] + findArgs(fileName, argv[1])

subprocess.call(
     argumentOf(
          waitForInputFrom(availableOptions, 'options')
     )
)

print('\n')