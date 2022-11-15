import re
import os

path = 'test/logs'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]
        
#print(files)

for old_file in files:
    file = open((os.path.join(path, old_file)), 'r')
    print(old_file)
    array = []

    while True:
        line = file.readline()
        if not line:
            break
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
            
    #cleprint(array)
            
    new_file = open(("test/logs/cleaned/" + old_file), 'w')
    new_file.writelines(array)
    new_file.close()
    