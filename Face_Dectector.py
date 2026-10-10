"""Local webcam facial-emotion service.


curl http://127.0.0.1:5000/emotion <-- returns the latest emotion as JSON.
Install with: pip install opencv-python deepface flask
DeepFace downloads its pretrained model on first use. Run this file and
request http://127.0.0.1:5000/emotion for the latest emotion as JSON.
"""

from threading import Event, Lock, Thread
import time

import cv2
from deepface import DeepFace
from flask import Flask, jsonify

app = Flask(__name__)
state_lock = Lock()
state = {"emotion": "unknown", "error": None, "updated_at": None}
stop_event = Event()


def analyze_webcam(camera_index=0, interval=0.5):
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        with state_lock:
            state["error"] = "Could not open webcam"
        return

    try:
        while not stop_event.is_set():
            ok, frame = camera.read()
            if not ok:
                with state_lock:
                    state["error"] = "Could not read webcam frame"
                stop_event.wait(interval)
                continue

            try:
                result = DeepFace.analyze(
                    img_path=frame,
                    actions=["emotion"],
                    enforce_detection=False,
                    detector_backend="opencv",
                    silent=True,
                )
                if isinstance(result, list):
                    result = result[0] if result else {}
                with state_lock:
                    state.update(
                        emotion=str(result.get("dominant_emotion", "unknown")).lower(),
                        error=None,
                        updated_at=time.time(),
                    )
            except Exception as exc:
                with state_lock:
                    state.update(emotion="unknown", error=f"Analysis failed: {exc}")
            stop_event.wait(interval)
    finally:
        camera.release()


@app.get("/emotion")
def get_emotion():
    with state_lock:
        return jsonify(dict(state))


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    Thread(target=analyze_webcam, daemon=True).start()
    try:
        app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)
    finally:
        stop_event.set()