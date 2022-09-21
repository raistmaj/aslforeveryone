import cv2
import numpy as np
import os
import string
# Create the directory structure
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/train"):
    os.makedirs("data/train")
if not os.path.exists("data/test"):
    os.makedirs("data/test")

for i in string.ascii_uppercase:
    if not os.path.exists("data/train/" + i):
        os.makedirs("data/train/"+i)
    if not os.path.exists("data/test/" + i):
        os.makedirs("data/test/"+i)

# Train or test 
mode = 'train'
directory = 'data/'+mode+'/'

count = {
    'a': len(os.listdir(directory+"/A")),
    'b': len(os.listdir(directory+"/B")),
    'c': len(os.listdir(directory+"/C")),
    'd': len(os.listdir(directory+"/D")),
    'e': len(os.listdir(directory+"/E")),
    'f': len(os.listdir(directory+"/F")),
    'g': len(os.listdir(directory+"/G")),
    'h': len(os.listdir(directory+"/H")),
    'i': len(os.listdir(directory+"/I")),
    'j': len(os.listdir(directory+"/J")),
    'k': len(os.listdir(directory+"/K")),
    'l': len(os.listdir(directory+"/L")),
    'm': len(os.listdir(directory+"/M")),
    'n': len(os.listdir(directory+"/N")),
    'o': len(os.listdir(directory+"/O")),
    'p': len(os.listdir(directory+"/P")),
    'q': len(os.listdir(directory+"/Q")),
    'r': len(os.listdir(directory+"/R")),
    's': len(os.listdir(directory+"/S")),
    't': len(os.listdir(directory+"/T")),
    'u': len(os.listdir(directory+"/U")),
    'v': len(os.listdir(directory+"/V")),
    'w': len(os.listdir(directory+"/W")),
    'x': len(os.listdir(directory+"/X")),
    'y': len(os.listdir(directory+"/Y")),
    'z': len(os.listdir(directory+"/Z"))
}

cap = cv2.VideoCapture(0)
interrupt = -1  
while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    # extract the frame
    h, w, _ = frame.shape
    start = abs(h - w) // 2
    
    roi = frame[(h // 2) - 250:(h // 2)+250, (w//2) - 250:(w//2)+250]

    #roi = frame[10:510, 220:720]
    cv2.imshow("test", roi)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
    if interrupt & 0xFF == ord('a'):
        cv2.imwrite(directory+'A/'+str(count['a'])+'.jpg', roi)
        count['a'] = count['a'] + 1
        print('A')
    if interrupt & 0xFF == ord('b'):
        cv2.imwrite(directory+'B/'+str(count['b'])+'.jpg', roi)
        count['b'] = count['b'] + 1
        print('B')
    if interrupt & 0xFF == ord('c'):
        cv2.imwrite(directory+'C/'+str(count['c'])+'.jpg', roi)
        count['c'] = count['c'] + 1
    if interrupt & 0xFF == ord('d'):
        cv2.imwrite(directory+'D/'+str(count['d'])+'.jpg', roi)
        count['d'] = count['d'] + 1
    if interrupt & 0xFF == ord('e'):
        cv2.imwrite(directory+'E/'+str(count['e'])+'.jpg', roi)
        count['e'] = count['e'] + 1
    if interrupt & 0xFF == ord('f'):
        cv2.imwrite(directory+'F/'+str(count['f'])+'.jpg', roi)
        count['f'] = count['f'] + 1
    if interrupt & 0xFF == ord('g'):
        cv2.imwrite(directory+'G/'+str(count['g'])+'.jpg', roi)
        count['g'] = count['g'] + 1
    if interrupt & 0xFF == ord('h'):
        cv2.imwrite(directory+'H/'+str(count['h'])+'.jpg', roi)
        count['h'] = count['h'] + 1
    if interrupt & 0xFF == ord('i'):
        cv2.imwrite(directory+'I/'+str(count['i'])+'.jpg', roi)
        count['i'] = count['i'] + 1
    if interrupt & 0xFF == ord('j'):
        cv2.imwrite(directory+'J/'+str(count['j'])+'.jpg', roi)
        count['j'] = count['j'] + 1
    if interrupt & 0xFF == ord('k'):
        cv2.imwrite(directory+'K/'+str(count['k'])+'.jpg', roi)
        count['k'] = count['k'] + 1
    if interrupt & 0xFF == ord('l'):
        cv2.imwrite(directory+'L/'+str(count['l'])+'.jpg', roi)
        count['l'] = count['l'] + 1
    if interrupt & 0xFF == ord('m'):
        cv2.imwrite(directory+'M/'+str(count['m'])+'.jpg', roi)
        count['m'] = count['m'] + 1
    if interrupt & 0xFF == ord('n'):
        cv2.imwrite(directory+'N/'+str(count['n'])+'.jpg', roi)
        count['n'] = count['n'] + 1
    if interrupt & 0xFF == ord('o'):
        cv2.imwrite(directory+'O/'+str(count['o'])+'.jpg', roi)
        count['o'] = count['o'] + 1
    if interrupt & 0xFF == ord('p'):
        cv2.imwrite(directory+'P/'+str(count['p'])+'.jpg', roi)
        count['p'] = count['p'] + 1
    if interrupt & 0xFF == ord('q'):
        cv2.imwrite(directory+'Q/'+str(count['q'])+'.jpg', roi)
        count['q'] = count['q'] + 1
    if interrupt & 0xFF == ord('r'):
        cv2.imwrite(directory+'R/'+str(count['r'])+'.jpg', roi)
        count['r'] = count['r'] + 1
    if interrupt & 0xFF == ord('s'):
        cv2.imwrite(directory+'S/'+str(count['s'])+'.jpg', roi)
        count['s'] = count['s'] + 1
    if interrupt & 0xFF == ord('t'):
        cv2.imwrite(directory+'T/'+str(count['t'])+'.jpg', roi)
        count['t'] = count['t'] + 1
    if interrupt & 0xFF == ord('u'):
        cv2.imwrite(directory+'U/'+str(count['u'])+'.jpg', roi)
        count['u'] = count['u'] + 1
    if interrupt & 0xFF == ord('v'):
        cv2.imwrite(directory+'V/'+str(count['v'])+'.jpg', roi)
        count['v'] = count['v'] + 1
    if interrupt & 0xFF == ord('w'):
        cv2.imwrite(directory+'W/'+str(count['w'])+'.jpg', roi)
        count['w'] = count['w'] + 1
    if interrupt & 0xFF == ord('x'):
        cv2.imwrite(directory+'X/'+str(count['x'])+'.jpg', roi)
        count['x'] = count['x'] + 1
    if interrupt & 0xFF == ord('y'):
        cv2.imwrite(directory+'Y/'+str(count['y'])+'.jpg', roi)
        count['y'] = count['y'] + 1
    if interrupt & 0xFF == ord('z'):
        cv2.imwrite(directory+'Z/'+str(count['z'])+'.jpg', roi)        
        count['z'] = count['z'] + 1
cap.release()
cv2.destroyAllWindows()