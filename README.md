# 🛰️ Satellite Image NDVI/NDWI Dashboard

This project is a Streamlit dashboard that analyzes satellite images using NDVI and NDWI.  
It allows users to upload one or two images, view vegetation and moisture levels, and compare environmental changes over time.

---

## 🌱 Features
- NDVI calculation (vegetation health)
- NDWI calculation with water-pixel masking (accurate moisture detection)
- Single-image interpretation
- Two-image comparison with AI-style trend prediction
- Simple interface for non-technical users

---

## 📦 Installation

### 1. Install Python
Make sure you have **Python 3.10 or newer** installed.

### 2. Install required packages
Open a terminal or command prompt inside the project folder and run:

pip install -r requirements.txt


This installs Streamlit, NumPy, and Pillow.

---

## ▶️ Running the Dashboard

Inside the project folder, run:

streamlit run dashboard.py


This will open the dashboard in your browser at:

http://localhost:8501

---

## 📸 How to Use

### **Single Image Analysis**
- Upload one satellite image
- View NDVI and NDWI (water-masked)
- Read interpretation of vegetation and moisture levels

### **Two-Image Comparison**
- Upload two images from different years
- View changes in NDVI and NDWI
- Read AI-style prediction of environmental trends

---

## 📁 Project Structure
aral-dashboard/
│
├── dashboard.py
├── requirements.txt
└── README.md


---

## 📱 Device Compatibility
Works on:
- Windows
- macOS
- Linux

No installation beyond Python and the required packages.

---

## 🌍 Notes
This dashboard runs locally unless deployed to Streamlit Cloud.
