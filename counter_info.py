
# 
# 
# lambda
# 
# 
printDemo = lambda title, lines: print(f'{title}\n' + '\n'.join(lines) + '\n')

# 
# 
# function
# 
# 
def printResultCount(count: int, item: str, itemsDescription: str):
    if count == 0:
        print(f'there is no {item}')
        return
    print(f'\nthere are {count} {item}\n{itemsDescription}')