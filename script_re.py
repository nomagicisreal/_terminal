import re

# without dot
substringFromDot = lambda source : re.search(r'\.(.*)', source).group(1)
substringToDot = lambda source : re.search(r'^(.*?)\.', source).group(1)