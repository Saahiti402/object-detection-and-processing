from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
import os
import cv2
import time

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")


@app.route("/")
def home():
    return {"message": "Backend running successfully"}


@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    filename = f"{int(time.time())}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    file.save(input_path)

    results = model(input_path)
    result = results[0]

    annotated_frame = result.plot()
    cv2.imwrite(output_path, annotated_frame)

    labels = []
    for box in result.boxes:
        cls_id = int(box.cls[0])
        labels.append(model.names[cls_id])

    return jsonify({
    "image_url": f"https://saahiti402-ai-suite.hf.space/output/{filename}",
    "labels": labels
})


@app.route("/annotations", methods=["POST"])
def annotations():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    filename = f"{int(time.time())}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(input_path)

    results = model(input_path)
    result = results[0]

    annotations_data = []

    for box in result.boxes:
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        annotations_data.append({
            "label": model.names[cls_id],
            "confidence": round(confidence, 2),
            "bbox": {
                "x1": round(x1, 2),
                "y1": round(y1, 2),
                "x2": round(x2, 2),
                "y2": round(y2, 2)
            }
        })

    return jsonify({"annotations": annotations_data})


@app.route("/cartoonize", methods=["POST"])
def cartoonize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    filename = f"{int(time.time())}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    output_filename = f"cartoon_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    image = cv2.imread(input_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9, 9
    )

    color = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    cv2.imwrite(output_path, cartoon)

    return jsonify({
        "image_url": f"https://saahiti402-ai-suite.hf.space/output/{output_filename}"
    })


@app.route("/video-detect", methods=["POST"])
def video_detect():
    if "file" not in request.files:
        return jsonify({"error": "No video uploaded"})

    file = request.files["file"]

    filename = f"{int(time.time())}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    output_filename = f"detected_{int(time.time())}.avi"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20

    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)
        processed_frame = results[0].plot()
        out.write(processed_frame)

    cap.release()
    out.release()

    return jsonify({
    "video_url": f"https://saahiti402-ai-suite.hf.space/output/{output_filename}"
    })


@app.route("/output/<filename>")
def get_output(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)