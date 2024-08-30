
# 
# 
# script_api has properties been used in other scripts.
# invoking by api.py, instead of integrating main() function call in script_api.py,
# prevent main() from being invoked by other scripts that import script_api.py
# 
# 
from script_api import main
main()