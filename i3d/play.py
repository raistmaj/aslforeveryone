
import cv2
import numpy as np
from pretrained_i3d import PreTrainedInception3d, add_top_layer


classes = ["hello", "yes", "no", "thank you"]
model = PreTrainedInception3d(include_top=False, pretrained_weights="rgb_imagenet_and_kinetics", dropout_prob=0.5,
                              input_shape=(64, 224, 224, 3), classes=len(classes))

model = add_top_layer(model, classes=len(classes), dropout_prob=0.5)
model.load_weights("model/20220923-0752-ASL105-oflow-i3d-top-last.h5")

video_source = cv2.VideoCapture(0)
frames = []
while True:
    re, frame = video_source.read()
    cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # exit
        break
    frame = cv2.resize(frame, (224, 224))
    frames.append(frame)
    if len(frames) == 64:
        prediction_result = model.predict(np.expand_dims(np.array(frames), axis=0))
        print(classes[np.argmax(prediction_result)])
        frames.pop(0)

video_source.release()
cv2.destryAllWindows()
