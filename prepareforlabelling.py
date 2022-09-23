import os
import string
import shutil
import uuid


# Gets the data from the train folder and rename the files adding 
# the last part of the path and a uuid
train_folder = "data/train/"
label_folder = "data/label/"

if not os.path.exists(label_folder):
    os.mkdir(label_folder)

for letter in string.ascii_uppercase:
    current_folder = os.path.join(train_folder, letter)
    for file in os.listdir(current_folder):
        shutil.copy(os.path.join(current_folder, file), os.path.join(label_folder, letter + '_' + str(uuid.uuid4()) + '.jpg'))
