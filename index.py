import os
import re
import subprocess
import sys

'''
Convert an aax file to mp3
'''

execution_context = sys.argv[1]
args = sys.argv[2:]

script_context = os.getcwd()

os.chdir(execution_context)

# Handle chapter extraction case
if args and (args[0] == '--chapters' or args[0] == '-c'):
    if len(args) < 2:
        print("Error: Please provide an AAX file when using --chapters/-c")
        sys.exit(1)
    aax_file = args[1]
    script_name = 'audibleconvert_chapters.sh'
else:
    if not args:
        print("Error: Please provide an AAX file")
        sys.exit(1)
    aax_file = args[0]
    script_name = 'audibleconvert.sh'

# Verify file extension
if not aax_file.lower().endswith('.aax'):
    print(f"Error: File '{aax_file}' must have .aax extension")
    sys.exit(1)

# Read activation bytes
activation_bytes_file = os.path.join(script_context, 'activation_bytes.txt')
if not os.path.exists(activation_bytes_file):
    setup_file = os.path.join(script_context, 'setup.md')
    if os.path.exists(setup_file):
        with open(setup_file) as f:
            print(f.read())
    else:
        print("Error: activation_bytes.txt not found")
    sys.exit(1)

with open(activation_bytes_file) as f:
    activation_bytes = f.read().strip()

if not activation_bytes:
    print("Error: activation_bytes.txt is empty")
    sys.exit(1)

# Execute the appropriate shell script with the aax file and activation bytes
subprocess.run([os.path.join(script_context, script_name), aax_file, activation_bytes])