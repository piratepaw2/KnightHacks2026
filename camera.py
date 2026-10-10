import threading

import cv2
from flask import Flask, Response

# Create the local web server and set the starting emotion.
app = Flask(__name__)
current_emotion = "neutral"


# GameMaker sends HTTP GET requests to this endpoint.
# Return the current emotion as plain text, such as "smile".
@app.get("/emotion")
def get_emotion():
    return Response(current_emotion, mimetype="text/plain")


def run_server():
    # Listen at http://127.0.0.1:5000 on this computer.
    # Disable the reloader so Flask does not restart the camera script.
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


def main():
    # Allow this function to update the emotion returned by the server.
    global current_emotion

    # Open the default webcam. Use another index if needed.
    camera = cv2.VideoCapture(0)

    try:
        if not camera.isOpened():
            raise RuntimeError("Could not open the webcam.")

        # Run Flask in the background while the main thread handles video.
        # The daemon thread stops when the program exits.
        threading.Thread(target=run_server, daemon=True).start()

        print("Click the webcam window and press:")
        print("1 = smile, 2 = angry, 3 = frown, 4 = neutral")
        print("Q = quit")

        while True:
            # Capture the next frame from the webcam.
            success, frame = camera.read()

            if not success:
                print("Could not read from the webcam.")
                break

            # Display the current emotion on the camera image.
            cv2.putText(
                frame,
                f"Emotion: {current_emotion}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Show the frame and check for a keyboard press.
            cv2.imshow("Webcam", frame)
            key = cv2.waitKey(1) & 0xFF

            # Keyboard controls simulate emotions for connection testing.
            # Automatic detection should eventually update
            # current_emotion based on the captured frame.
            if key == ord("q"):
                break
            elif key == ord("1"):
                current_emotion = "smile"
            elif key == ord("2"):
                current_emotion = "angry"
            elif key == ord("3"):
                current_emotion = "frown"
            elif key == ord("4"):
                current_emotion = "neutral"
    finally:
        # Release the webcam and close its windows, even after an error.
        camera.release()
        cv2.destroyAllWindows()


# Start the program only when this file is run directly.
if __name__ == "__main__":
    main()