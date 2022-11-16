# Script to clean logs created from mitm-proxy
import re
import os

# Path to the logs, that needed to be cleaned
path = 'test/logs'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]
        
# Iterate over all files in the directory
for old_file in files:
    file = open((os.path.join(path, old_file)), 'r')
    print(old_file)
    array = []

    # Operations on every line within the file
    while True:
        line = file.readline()
        if not line:
            break
        # Regex operations and string replacements
        x = re.search("INFO(.*)INFO", line)
        x1 = re.search("b'------WebKitFormBoundary", line)
        if x or x1:
            continue
        line = re.sub("\| content: b", " content:", line)
        z = re.search("INFO", line)
        
        if z:
            line = line.replace(' - ', ' ')
            line = line.replace(': ', ' ')
            line = line.replace('\n', ' headers:')
        
        line = line.replace(': ', ':')
        line = line.replace(', ', ',')

        
        
        
        array.append(line)
            
    # Write out a cleaned version of the file            
    new_file = open(("test/logs/cleaned/" + old_file), 'w')
    new_file.writelines(array)
    new_file.close()
    