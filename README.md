# Paul Heffner and Elena Houser

Install the webcam dependencies:

pip install -r requirements.txt

This project uses OpenCV Haar cascades for face detection and MediaPipe face landmarks for geometry-based mouth-shape recognition. The app exposes:

curl http://127.0.0.1:5000/face_shape

It returns JSON such as {"face_shape": "smile", "emotion": "smile"} while the webcam is running. Mouth-open detection is reported as "surprise" and the neutral state is "neutral".

a webcam
Python 3.11
the required packages installed
camera permissions enabled

python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python Face_Dectector.py

run:

cd "C:\Users\theme\Documents\Educational Information\Fall 2026\KnightHacks26\KnightHacks2026"
.\.venv\Scripts\Activate.ps1
python Face_Dectector.py