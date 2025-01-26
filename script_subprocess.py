import subprocess

# 
# 
# lambda
# 
# 
stdoutMessageOf = lambda args : subprocess.run(args, capture_output=True).stdout.decode()
stderrMessageOf = lambda args : subprocess.run(args, capture_output=True).stderr.decode()

def callThenRemoveArgs2(args: list):
    subprocess.call(args)
    subprocess.call(['rm', args[2]])