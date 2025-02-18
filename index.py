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

# Execute the appropriate shell script with the aax file
subprocess.run([os.path.join(script_context, script_name), aax_file])