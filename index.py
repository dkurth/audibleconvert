import os
import re
import subprocess
import sys

'''
Convert an aax file to mp3
'''


def load_activation_profiles(path):
    profiles = {}
    default_profile = None
    current_profile = None

    with open(path) as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith('[') and line.endswith(']'):
                current_profile = line[1:-1].strip()
                if current_profile and current_profile not in profiles:
                    profiles[current_profile] = None
                    if default_profile is None:
                        default_profile = current_profile
            else:
                if current_profile is not None and profiles.get(current_profile) is None:
                    profiles[current_profile] = line

    # Remove any profiles that never got a value
    profiles = {k: v for k, v in profiles.items() if v}

    if default_profile is not None and default_profile not in profiles and profiles:
        # Fallback to the first profile that actually has a value
        default_profile = next(iter(profiles.keys()))

    return profiles, default_profile


execution_context = sys.argv[1]
args = sys.argv[2:]

script_context = os.getcwd()

os.chdir(execution_context)

# Handle chapter extraction flag and profile/file arguments
is_chapters = False
if args and (args[0] == '--chapters' or args[0] == '-c'):
    is_chapters = True
    args = args[1:]

if not args:
    print("Error: Please provide an AAX file")
    sys.exit(1)

profile_name = None
if len(args) == 1:
    aax_file = args[0]
elif len(args) == 2:
    profile_name, aax_file = args
else:
    print("Error: Too many arguments.")
    print("Usage: audibleconvert [--chapters|-c] [profile] <file.aax>")
    sys.exit(1)

script_name = 'audibleconvert_chapters.sh' if is_chapters else 'audibleconvert.sh'

# Verify file extension
if not aax_file.lower().endswith('.aax'):
    print(f"Error: File '{aax_file}' must have .aax extension")
    sys.exit(1)

# Read activation bytes from activation_bytes.yml
activation_bytes_file = os.path.join(script_context, 'activation_bytes.yml')
if not os.path.exists(activation_bytes_file):
    setup_file = os.path.join(script_context, 'setup.md')
    if os.path.exists(setup_file):
        with open(setup_file) as f:
            print(f.read())
    else:
        print("Error: activation_bytes.yml not found")
    sys.exit(1)

profiles, default_profile = load_activation_profiles(activation_bytes_file)

if not profiles:
    print("Error: activation_bytes.yml is empty or has no valid profiles")
    sys.exit(1)

if profile_name is None:
    profile_name = default_profile

if profile_name not in profiles:
    print(f"Error: profile '{profile_name}' not found in activation_bytes.yml")
    print("Available profiles: " + ", ".join(sorted(profiles.keys())))
    sys.exit(1)

activation_bytes = profiles[profile_name].strip()

if not activation_bytes:
    print(f"Error: activation_bytes for profile '{profile_name}' is empty")
    sys.exit(1)

# Execute the appropriate shell script with the aax file and activation bytes
subprocess.run([os.path.join(script_context, script_name), aax_file, activation_bytes])