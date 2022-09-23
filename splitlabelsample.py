import os
import pathlib
import shutil
from collections import defaultdict
# given a folder with tagged images
# it will split the sample into two folders
# train and test. 

train_percentage = 80
test_percentage = 100 - train_percentage

label_folder = 'data/label_copy'
train_folder = os.path.join(label_folder, 'train')
test_folder = os.path.join(label_folder, 'test')
if not os.path.exists(train_folder):
    os.mkdir(train_folder)

if not os.path.exists(test_folder):
    os.mkdir(test_folder)

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
    total_files = len(list_of_files)
    train_number = (total_files * train_percentage) // 100
    test_number = total_files - train_number
    i = 0
    for file in list_of_files:
        jpeg_file = file
        xml_file = os.path.splitext(file)[0] + '.xml'
        destination_jpeg = os.path.join(train_folder, jpeg_file)
        destination_xml = os.path.join(train_folder, xml_file)
        if i >= train_number:
            destination_jpeg = os.path.join(test_folder, jpeg_file)
            destination_xml = os.path.join(test_folder, xml_file)
        shutil.copy(os.path.join(label_folder, jpeg_file), destination_jpeg)
        shutil.copy(os.path.join(label_folder, xml_file), destination_xml)
        i += 1