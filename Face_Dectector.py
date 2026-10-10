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

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
DETECTION_SCALE = 0.5
FRAME_SKIP = 2
PROCESS_INTERVAL = 0.05

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
shape_history = deque(maxlen=4)
face_history = deque(maxlen=3)
mouth_open_history = deque(maxlen=3)
face_mesh = None
last_face_box = None


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
    except Exception:
        pass

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
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                camera.set(cv2.CAP_PROP_FPS, 30)
                return camera, index
            camera.release()

    return None, None


def locate_face(frame):
    global last_face_box
    if frame is None or frame.size == 0:
        return None

    try:
        cascade_path = ensure_haar_cascade()
    except FileNotFoundError:
        return None

    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        return None

    source_h, source_w = frame.shape[:2]
    target_w = max(1, int(source_w * DETECTION_SCALE))
    target_h = max(1, int(source_h * DETECTION_SCALE))
    small_frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    search_regions = [gray]
    if last_face_box is not None:
        x, y, w, h = last_face_box
        pad = int(max(w, h) * 0.35)
        x0 = max(0, int(x * DETECTION_SCALE) - pad)
        y0 = max(0, int(y * DETECTION_SCALE) - pad)
        x1 = min(target_w, int((x + w) * DETECTION_SCALE) + pad)
        y1 = min(target_h, int((y + h) * DETECTION_SCALE) + pad)
        if x1 > x0 and y1 > y0:
            search_regions.append(gray[y0:y1, x0:x1])

    best_box = None
    for region_index, region in enumerate(search_regions):
        faces = face_cascade.detectMultiScale(
            region,
            scaleFactor=1.08,
            minNeighbors=2,
            minSize=(20, 20),
        )
        if len(faces) == 0:
            continue
        x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
        if region_index == 0:
            box = (x, y, w, h)
        else:
            box = (x + x0, y + y0, w, h)
        best_box = box
        break

    if best_box is None:
        return None

    x, y, w, h = best_box
    x = int(round(x / DETECTION_SCALE))
    y = int(round(y / DETECTION_SCALE))
    w = int(round(w / DETECTION_SCALE))
    h = int(round(h / DETECTION_SCALE))
    last_face_box = (x, y, w, h)
    padding = int(0.2 * max(w, h))
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

        # Direct open-mouth detection should dominate the classifier. If the mouth is
        # sufficiently open and stays open for at least one frame, classify it as
        # surprise regardless of the subtle smile/frown geometry.
        # 2x easier detection: a mouth that is clearly open should trigger surprise
        # when the vertical distance is roughly 1/4 of the mouth width.
        mouth_open = mouth_height > 0.030 and mouth_width > 0.06 and mouth_height >= (mouth_width * 0.25)
        mouth_open_history.append(1 if mouth_open else 0)
        mouth_open_streak = sum(mouth_open_history)

        frown_score = 0.0
        if mouth_corner_drop > 0.01:
            frown_score += mouth_corner_drop * 16.0
        if mouth_height < 0.09:
            frown_score += (0.09 - mouth_height) * 5.0
        if mouth_ratio < 1.2:
            frown_score += (1.2 - mouth_ratio) * 1.5

        if mouth_open and mouth_open_streak >= 1:
            return "surprise", min(0.99, 0.72 + max(0.0, mouth_open_score) + max(0.0, eye_open_score))
        if smile_score > 0.12 and mouth_corner_lift > 0.00:
            return "smile", min(0.99, 0.55 + smile_score)

        if mouth_corner_drop > 0.008 and frown_score > 0.12:
            return "frown", min(0.99, 0.62 + frown_score)
        if mouth_height > mouth_width * 0.92 and mouth_corner_avg_y > mouth_center_y + 0.005:
            return "frown", min(0.99, 0.62 + (mouth_height / max(0.0001, mouth_width + 0.001)))
        if widened_eyes and mouth_ratio > 0.7:
            return "surprise", min(0.99, 0.7 + (mouth_ratio * 0.2))

        return "neutral", 0.8
    except Exception:
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


def analyze_webcam(camera_index=0, interval=PROCESS_INTERVAL):
    camera, actual_index = open_camera(camera_index)
    if camera is None:
        with state_lock:
            state["camera_index"] = None
            state["error"] = "Could not open webcam; check camera permissions or camera index"
        return

    with state_lock:
        state["camera_index"] = actual_index

    frame_counter = 0
    try:
        while not stop_event.is_set():
            ok, frame = camera.read()
            if not ok:
                with state_lock:
                    state["error"] = "Could not read webcam frame"
                stop_event.wait(interval)
                continue

            frame_counter += 1
            if frame_counter % FRAME_SKIP != 0:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_event.set()
                    break
                continue

            if frame.shape[0] != FRAME_HEIGHT or frame.shape[1] != FRAME_WIDTH:
                frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT), interpolation=cv2.INTER_AREA)

            shape, confidence, face_found, error = classify_face(frame)
            face_history.append(1 if face_found else 0)
            face_detected = sum(face_history) >= 2

            if face_detected and shape != "unknown":
                shape_history.append(shape)
                vote_counts = Counter(shape_history)
                predicted_shape, predicted_count = max(
                    vote_counts.items(), key=lambda item: (item[1], item[0])
                )
                if confidence >= 0.72 or predicted_count >= 2 or len(shape_history) >= 3:
                    selected_shape = predicted_shape
                else:
                    selected_shape = shape
            else:
                shape_history.clear()
                selected_shape = "unknown"

            # Release build: no live camera preview or debug overlay. The server only
            # exposes the latest emotion state through the HTTP endpoint.
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