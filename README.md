# 🚗 License Plate Detector

A smart computer vision project that detects vehicles and reads license plates from live or recorded video using YOLOv8 and OCR, then uploads the results to a database. Built with Python, OpenCV, and Ultralytics YOLO.

## ✨ Features

- 🎯 Real-time vehicle and license plate detection using YOLOv8
- 🔡 OCR for reading license plate text
- 🎥 Works with both live webcam and pre-recorded video
- 🧭 Vehicle tracking with the SORT algorithm
- ☁️ Uploads license plate data to a remote database
- 🖼 Saves frames where vehicles are detected
- 🧪 Visualization tools for plate preprocessing and OCR debugging

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/karthick1005/license-plate-detector.git
cd license-plate-detector
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR (required for `pytesseract`)

- **Ubuntu/Debian:**
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **macOS:**
  ```bash
  brew install tesseract
  ```
- **Windows:**
  - Download installer: https://github.com/tesseract-ocr/tesseract
  - Add the Tesseract installation directory to your PATH.

---

## 📁 Project Structure

```
├── models/
│   └── license_plate_detector.pt        # YOLOv8 model for license plates
├── cars.xml                             # Haar cascade for vehicle detection
├── util.py                              # Utility functions (OCR, helpers)
├── sort.py                              # SORT tracking algorithm
├── Restapi.py                           # Uploads data to database/API
├── sample2.mp4                          # Test video
├── detected_vehicle.png                 # Frame capture (temp)
├── main.py                              # Main script
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## 🚀 Usage

### Live Webcam Detection

```bash
python main.py
```
Then enter `0` when prompted.

### Recorded Video Detection

```bash
python main.py
```
Then enter `1` when prompted.

---

## ⚙️ Customization

- 🔧 Edit `uploadtodatabase()` in `Restapi.py` to match your API or database backend.
- 🧠 You can enhance `read_license_plate()` in `util.py` for better OCR accuracy or use a different OCR engine.
- 🖼 Uncomment `visualize_plot()` in `main.py` to visualize preprocessing steps for license plates.

---

## 🧠 Models

- **YOLOv8 (`yolov8n.pt`)** is used for vehicle detection.
- A custom-trained YOLOv8 model (`license_plate_detector.pt`) is used to detect license plates.
- **SORT** is used to associate license plates with specific vehicles.

---

## 📄 Requirements

Dependencies listed in `requirements.txt`:

```
ultralytics==8.0.20
opencv-python
numpy
matplotlib
pytesseract
requests
```

---

## 📝 License

This project is open-source and licensed under the MIT License. Feel free to use and modify it.

---

## 🙌 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [SORT Algorithm](https://github.com/abewley/sort)

---

Happy detecting! 🎉
