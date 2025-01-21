# 
# 
# 
# 
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
        errorMessage: str = f'no such option: {o}\n'

        try:
             name = optionNames[int(o)-1]
             return [options[name], name]
        except TypeError:       errorMessage += f'please input integer instead of {o}'
        except IndexError:      errorMessage += f'require 0 < {o} < {len(options)})'
        except Exception as e:  errorMessage = e
        print(errorMessage)


def whileEnsureLocation(cwd: str, travelOn):
    while True:
        destination = input(f'location (default: {cwd}): ')

        args = destination.split()
        argsLength = len(args)
        if argsLength == 0: return
        if argsLength == 1:
            travelOn(args[0])
            return
        
        if argsLength == 2:
            command = args[0]
            if command == 'cd':
                travelOn(args[1])
                continue
        
        print(
            f"unknown command: {args}\n"
            "USAGES:\n"
            "\t1. press enter to ensure the current location\n"
            "\t2. 'cd [your_path]'\n"
        )
