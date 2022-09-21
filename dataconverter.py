import cv2
import os
import string

# transform the data set folder into BW with edges
input_train_set = 'data/train/'
input_validation_set = 'data/test/'

bw_folder = 'data/bw/'
output_train_set = 'data/bw/train/'
output_validation_set = 'data/bw/test/'


if not os.path.exists("data"):
    exit
if not os.path.exists(input_train_set):
    exit
if not os.path.exists(input_validation_set):
    exit

for i in string.ascii_uppercase:
    if not os.path.exists(input_train_set + i):
        exit
    if not os.path.exists(input_validation_set + i):
        exit

if not os.path.exists(bw_folder):
    os.makedirs(bw_folder)
if not os.path.exists(output_train_set):
    os.makedirs(output_train_set)
if not os.path.exists(output_validation_set):
    os.makedirs(output_validation_set)

for i in string.ascii_uppercase:
    if not os.path.exists(output_train_set + i):
        os.makedirs(output_train_set+i)
    if not os.path.exists(output_validation_set + i):
        os.makedirs(output_validation_set+i)


for i in string.ascii_uppercase:
    # train
    current_folder = input_train_set + i
    current_output_folder = output_train_set + i

    for current_file in os.listdir(current_folder):
        if os.path.isdir(os.path.join(current_folder, current_file)):
            continue

        if current_file == '.DS_Store':
            continue

        print('Processing ' + os.path.join(current_folder, current_file))
        # load the image as greyscale
        current_image = cv2.imread(os.path.join(current_folder, current_file), 0)

        #Sobel Edge Detection
        image_blur = cv2.GaussianBlur(current_image,(3,3), 0)

        sobelxy = cv2.Sobel(src=image_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

        edges = sobelxy
        # # Canny edge detection
        # edges = cv2.Canny(image=current_image, threshold1=100, threshold2=100)

        print('Writting ' + os.path.join(current_output_folder, current_file))
        resized = cv2.resize(edges, (256,256), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(current_output_folder, current_file), resized)
    
    # test
    current_folder = input_validation_set + i
    current_output_folder = output_validation_set + i

    for current_file in os.listdir(current_folder):
        if os.path.isdir(os.path.join(current_folder, current_file)):
            continue
        
        if current_file == '.DS_Store':
            continue

        print('Processing ' + os.path.join(current_folder, current_file))
        # load the image as greyscale
        current_image = cv2.imread(os.path.join(current_folder, current_file), 0)

        #Sobel Edge Detection
        image_blur = cv2.GaussianBlur(current_image,(3,3), 0)
        sobelxy = cv2.Sobel(src=image_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

        edges = sobelxy
        # # Canny edge detection
        # edges = cv2.Canny(image=current_image, threshold1=150, threshold2=100)

        print('Writting ' + os.path.join(current_output_folder, current_file))
        resized = cv2.resize(edges, (256,256), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(current_output_folder, current_file), resized)


