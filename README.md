#  AI Vision Suite

AI Vision Suite is a **full-stack computer vision web application** built using **React, Flask, YOLOv8, and OpenCV**.

It provides multiple intelligent image and video processing features through a clean, modern, and user-friendly interface.

---

##  Features

###  Object Detection
Upload an image and detect multiple objects using **YOLOv8**.

- Detects multiple objects
- Displays labels
- Returns processed image with bounding boxes

---

###  Annotations
Generate detailed annotation information for uploaded images.

- Object labels
- Confidence score
- Bounding box coordinates

---

###  Cartoonization
Convert normal images into cartoon-style visuals using OpenCV image processing techniques.

- Edge detection
- Bilateral filtering
- Cartoon effect output

---

###  Video Detection
Upload a video and perform frame-by-frame object detection.

- Video frame processing
- YOLO-based object detection
- Download processed video output

---

##  Tech Stack

### Frontend
- React.js
- Axios
- CSS

### Backend
- Flask
- Flask-CORS
- OpenCV
- Ultralytics YOLOv8
- Python

---


##  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Vision-Suite.git
cd AI-Vision-Suite
```
### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```
### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```
### Required Python Packages
```bash
pip install flask flask-cors ultralytics opencv-python
```
## Model Used 
This project uses:
```bash
yolov8n.pt
```
## Future Enhancements
1. Live webcam detection
2. Face detection
3. OCR text extraction
4. AI filters
5. Cloud deployment

