
from flask import Flask, render_template, jsonify, Response
import cv2, random

app = Flask(__name__)
cap = cv2.VideoCapture(0)
camera_running = True
history = []

def gen_frames():
    global camera_running
    while True:
        success, frame = cap.read()
        if not success:
            break
        if not camera_running:
            # still read frames to keep camera warm
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/toggle_camera")
def toggle_camera():
    global camera_running
    camera_running = not camera_running
    return jsonify({"status": camera_running})

@app.route("/face")
def face():
    return jsonify({"face": random.randint(30,90)})

@app.route("/voice")
def voice():
    return jsonify({"voice": random.randint(30,90)})

@app.route("/analyze")
def analyze():
    face = random.randint(30,90)
    voice = random.randint(30,90)
    final = (face + voice)//2
    history.append({"face": face, "voice": voice, "final": final})
    if len(history) > 10:
        history.pop(0)
    return jsonify({"face": face, "voice": voice, "final": final})

@app.route("/history")
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
