from genericpath import isfile
import os
import string
import shutil
import pathlib
from collections import defaultdict

# Given an input folder with images it will trim it down to 100 
# per prefix. If it was already tagged, it will not remove it but
# it still counts
label_folder = "data/label_copy/"
file_by_prefix = defaultdict(list)
for file in os.listdir(label_folder):
    if not os.path.isfile(os.path.join(label_folder,file)):
        continue
    file_extension = pathlib.Path(file).suffix
    if file_extension != '.jpg':
        continue
    last_underscore = file.rfind('_')
    if last_underscore == -1:
        continue
    current_prefix = file[:last_underscore]
    file_by_prefix[current_prefix].append(file)

for key in file_by_prefix:
    list_of_files = file_by_prefix[key]
    if len(list_of_files) > 100:
        i = 0
        for single_file in list_of_files:
            i += 1
            xml_version = os.path.splitext(single_file)[0] + '.xml'
            if os.path.exists(os.path.join(label_folder, xml_version)):
                print(single_file + ' has .xml file, ignoring it')
                continue
            if i > 100:
                # Delete
                print('Deleting', single_file, 'because we have more than 100 and it has not .xml file')
                os.remove(os.path.join(label_folder, single_file))
            
