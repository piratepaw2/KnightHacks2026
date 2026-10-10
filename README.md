# Paul Heffner, Elena Houser, Jackson Snyder

Install the webcam dependencies:

pip install -r requirements.txt

This project uses OpenCV Haar cascades for face detection and MediaPipe face landmarks for geometry-based mouth-shape recognition. The app exposes:

curl http://127.0.0.1:5000/face_shape

It returns JSON such as {"face_shape": "smile", "emotion": "smile"} while the webcam is running. Mouth-open detection is reported as "surprise" and the neutral state is "neutral".
