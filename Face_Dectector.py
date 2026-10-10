"""Local webcam mouth-shape detector.

curl http://127.0.0.1:5000/face_shape <-- returns the latest mouth contour label as JSON.
Install with: pip install opencv-python mediapipe flask
Run this file and request the endpoint to get the latest label: smile, neutral,
frown, or surprise.

py -m pip uninstall opencv-python opencv-contrib-python opencv-python-headless -y
py -m pip install --force-reinstall opencv-python mediapipe

"""

from collections import Counter, deque
import os
import time
import urllib.request
from pathlib import Path
from threading import Event, Lock, Thread

import cv2
import numpy as np
from flask import Flask, jsonify

MP_IMPORT_ERROR = None
try:
    import mediapipe as mp
    if not hasattr(mp, "solutions"):
        raise AttributeError("mediapipe.solutions is unavailable - reinstall MediaPipe with a supported Python version")
except Exception as exc:  # pragma: no cover - optional dependency
    mp = None
    MP_IMPORT_ERROR = exc

app = Flask(__name__)
state_lock = Lock()
state = {
    "emotion": "unknown",
    "face_shape": "unknown",
    "face_detected": False,
    "confidence": 0.0,
    "error": None,
    "updated_at": None,
    "camera_index": None,
}
stop_event = Event()
shape_history = deque(maxlen=7)
face_history = deque(maxlen=5)
face_mesh = None


def ensure_haar_cascade():
    """Ensure the OpenCV Haar cascade XML is available for face detection."""
    candidates = []
    if hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
        candidates.append(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
    candidates.append(os.path.join(os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml"))

    project_data_dir = Path(__file__).resolve().parent / "data" / "haarcascades"
    project_data_path = project_data_dir / "haarcascade_frontalface_default.xml"
    candidates.append(str(project_data_path))

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    project_data_dir.mkdir(parents=True, exist_ok=True)
    url = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml"
    fallback_path = str(project_data_path)
    try:
        urllib.request.urlretrieve(url, fallback_path)
        if os.path.exists(fallback_path):
            return fallback_path
    except Exception as exc:  # pragma: no cover - network-dependent fallback
        print(f"DEBUG: unable to download Haar cascade XML: {exc}")

    raise FileNotFoundError(
        "OpenCV Haar cascade XML is missing. Install opencv-contrib-python or download "
        "haarcascade_frontalface_default.xml into the project data/haarcascades folder."
    )


def open_camera(camera_index=0):
    attempts = []
    if camera_index is not None:
        attempts.append(camera_index)
    attempts.extend([0, 1, 2, 3])

    seen = set()
    for index in attempts:
        if index in seen:
            continue
        seen.add(index)

        for backend in (cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY):
            camera = cv2.VideoCapture(index, backend)
            if camera.isOpened():
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                return camera, index
            camera.release()

    return None, None


def locate_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    try:
        cascade_path = ensure_haar_cascade()
    except FileNotFoundError as exc:
        print(f"DEBUG: {exc}")
        return None

    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        print(f"DEBUG: Haar cascade failed to load: {cascade_path}")
        return None

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30),
    )
    print(f"DEBUG: cascade path={cascade_path} faces_detected={len(faces)}")
    if len(faces) == 0:
        return None

    x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
    padding = int(0.15 * max(w, h))
    x = max(0, x - padding)
    y = max(0, y - padding)
    x2 = min(frame.shape[1], x + w + (padding * 2))
    y2 = min(frame.shape[0], y + h + (padding * 2))
    return frame[y:y2, x:x2]


def normalize_face(face):
    if face is None or face.size == 0:
        return None

    face = cv2.resize(face, (224, 224), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.equalizeHist(gray)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def estimate_face_shape_from_landmarks(frame, face):
    global face_mesh
    if mp is None or not hasattr(mp, "solutions") or frame is None or frame.size == 0:
        print(f"DEBUG: MediaPipe is unavailable: {MP_IMPORT_ERROR or 'mediapipe.solutions is missing'}")
        return None

    try:
        if face_mesh is None:
            face_mesh = mp.solutions.face_mesh.FaceMesh(
                static_image_mode=False,
                refine_landmarks=True,
                max_num_faces=1,
                min_detection_confidence=0.4,
                min_tracking_confidence=0.4,
            )

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            print("DEBUG: FaceMesh found no face landmarks in frame")
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        def point(idx):
            lm = landmarks[idx]
            return np.array([lm.x, lm.y], dtype=np.float32)

        mouth_left = point(61)
        mouth_right = point(291)
        mouth_top = point(13)
        mouth_bottom = point(14)
        left_eye_top = point(159)
        left_eye_bottom = point(145)
        right_eye_top = point(386)
        right_eye_bottom = point(374)
        left_brow = point(70)
        right_brow = point(300)

        mouth_width = float(np.linalg.norm(mouth_right - mouth_left))
        mouth_height = float(np.linalg.norm(mouth_bottom - mouth_top))
        left_eye_height = float(np.linalg.norm(left_eye_bottom - left_eye_top))
        right_eye_height = float(np.linalg.norm(right_eye_bottom - right_eye_top))
        eye_height = (left_eye_height + right_eye_height) / 2.0
        brow_gap = float(np.linalg.norm(left_brow - right_brow))
        mouth_center_y = (mouth_top[1] + mouth_bottom[1]) / 2.0
        mouth_corner_avg_y = (mouth_left[1] + mouth_right[1]) / 2.0

        mouth_ratio = mouth_width / max(0.0001, mouth_height + 0.001)
        smile_score = mouth_ratio - 1.0
        mouth_open_score = mouth_height - 0.08
        eye_open_score = (eye_height * 3.2) - 0.18
        widened_eyes = brow_gap > 0.14 and eye_open_score > 0.0
        mouth_corner_lift = mouth_center_y - mouth_corner_avg_y
        mouth_corner_drop = mouth_corner_avg_y - mouth_center_y

        # Convert the mouth geometry into a more explicit frown signal.
        # A strong frown usually pulls both corners downward and makes the mouth
        # appear compact rather than wide/open.
        frown_score = 0.0
        if mouth_corner_drop > 0.01:
            frown_score += mouth_corner_drop * 16.0
        if mouth_height < 0.09:
            frown_score += (0.09 - mouth_height) * 5.0
        if mouth_ratio < 1.2:
            frown_score += (1.2 - mouth_ratio) * 1.5

        if mouth_height > 0.075 and eye_open_score > 0.00 and mouth_width > 0.12:
            return "surprise", min(0.99, 0.58 + max(0.0, mouth_open_score) + max(0.0, eye_open_score))
        if smile_score > 0.12 and mouth_corner_lift > 0.00:
            return "smile", min(0.99, 0.55 + smile_score)

        if mouth_corner_drop > 0.008 and frown_score > 0.12:
            return "frown", min(0.99, 0.62 + frown_score)
        if mouth_height > mouth_width * 0.92 and mouth_corner_avg_y > mouth_center_y + 0.005:
            return "frown", min(0.99, 0.62 + (mouth_height / max(0.0001, mouth_width + 0.001)))
        if widened_eyes and mouth_ratio > 0.7:
            return "surprise", min(0.99, 0.7 + (mouth_ratio * 0.2))

        return "neutral", 0.8
    except Exception as exc:
        print(f"DEBUG: landmark classification exception: {exc}")
        return None


def classify_face(frame):
    face = locate_face(frame)
    if face is None:
        return "unknown", 0.0, False, "No face detected in frame"

    landmark_prediction = estimate_face_shape_from_landmarks(frame, face)
    if landmark_prediction is not None:
        shape, confidence = landmark_prediction
        return shape, float(confidence), True, None

    return "neutral", 0.5, True, "Landmarks were weak; defaulted to neutral"


def analyze_webcam(camera_index=0, interval=0.5):
    camera, actual_index = open_camera(camera_index)
    if camera is None:
        with state_lock:
            state["camera_index"] = None
            state["error"] = "Could not open webcam; check camera permissions or camera index"
        return

    with state_lock:
        state["camera_index"] = actual_index

    try:
        while not stop_event.is_set():
            ok, frame = camera.read()
            if not ok:
                with state_lock:
                    state["error"] = "Could not read webcam frame"
                stop_event.wait(interval)
                continue

            shape, confidence, face_found, error = classify_face(frame)
            face_history.append(1 if face_found else 0)
            face_detected = sum(face_history) >= 2

            if face_detected and shape != "unknown":
                shape_history.append(shape)
                vote_counts = Counter(shape_history)
                predicted_shape, predicted_count = max(
                    vote_counts.items(), key=lambda item: (item[1], item[0])
                )
                if predicted_count >= 2 or len(shape_history) >= 3:
                    selected_shape = predicted_shape
                else:
                    selected_shape = shape
            else:
                selected_shape = "unknown"

            if face_found:
                print(f"DEBUG: face_found={face_found}, shape={shape}, confidence={confidence}, error={error}")
            else:
                print(f"DEBUG: face_found={face_found}, error={error}")

            display_label = selected_shape if face_detected and selected_shape != "unknown" else "No face"
            cv2.putText(
                frame,
                f"Face Shape: {display_label}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            # Temporary debug window to inspect the live camera feed.
            cv2.imshow("Face Debug", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                stop_event.set()
                break

            with state_lock:
                state.update(
                    emotion=selected_shape,
                    face_shape=selected_shape,
                    face_detected=face_detected,
                    confidence=confidence,
                    error=error if face_detected else "No face detected",
                    updated_at=time.time(),
                )

            stop_event.wait(interval)
    finally:
        cv2.destroyAllWindows()
        camera.release()


@app.get("/face_shape")
def get_face_shape():
    with state_lock:
        payload = dict(state)
        payload["face_shape"] = payload.get("face_shape") or payload.get("emotion")
        return jsonify(payload)


@app.get("/emotion")
def get_emotion():
    return get_face_shape()


@app.get("/health")
def health():
    with state_lock:
        camera_available = state.get("camera_index") is not None
    return jsonify(status="ok", camera_available=camera_available)


if __name__ == "__main__":
    Thread(target=analyze_webcam, daemon=True).start()
    try:
        app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)
    finally:
        stop_event.set()