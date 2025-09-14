# AI-Virtual-Painter
An AI-powered Virtual Painter using Python, OpenCV, and MediaPipe. Draw on a digital canvas with hand gestures: select colors by moving fingers to the top bar, use index finger to paint, and eraser mode to clear. Real-time hand tracking enables touchless drawing with smooth interaction.

# 🎨 AI Virtual Painter

An AI-powered **gesture-controlled drawing application** built with Python, OpenCV, and MediaPipe.  
Control your brush with hand movements — no mouse or stylus needed!  

## 🚀 Features
- Hand tracking with **MediaPipe Hands**  
- **Drawing Mode**: Use your index finger to paint  
- **Selection Mode**: Use index + middle finger to pick colors  
- **Eraser Mode**: Select black to erase drawings  
- On-screen **color palette (Blue, Green, Red, Eraser)**  
- Real-time webcam feed with merged canvas  

## 🛠️ Tech Stack
- Python  
- OpenCV  
- MediaPipe  
- NumPy  

## 🎮 Controls
- **Index finger up** → Draw on screen  
- **Index + Middle finger up** → Select color/eraser (move to top bar)  
- **Eraser selected** → Remove drawings  
- Press **Q** → Quit  

## 📦 Installation
```bash
pip install opencv-python mediapipe numpy
