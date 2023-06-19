import sys
import cv2 
import imutils
# GS streamer
# import subprocess
from yoloDet_traffic import YoloTRT

# Codedao

# def alarm():

#     # Define the GStreamer pipeline as a string
#     pipeline = 'filesrc location=sine.ogg ! oggdemux ! vorbisdec ! audioconvert ! audioresample ! pulsesink'

#     # Run the gst-launch-1.0 command using subprocess
#     process = subprocess.Popen(['gst-launch-1.0', '-v', pipeline], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # Wait for the process to finish and capture the output
#     stdout, stderr = process.communicate()

#     # Print the output
#     print('stdout:', stdout)
#     print('stderr:', stderr)

## Ending


# use path for library and engine file
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/USTH_model5s.engine", conf=0.5, yolo_ver="v5")

cap = cv2.VideoCapture("videos/traffic_test.mp4")

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)
    for obj in detections:
         print(obj['class'], obj['conf'], obj['box'])
    # alarm()
    print("FPS: {} sec".format(1/t))
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()