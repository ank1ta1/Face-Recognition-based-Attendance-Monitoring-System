# Face-Recognition-based-Attendance-Monitoring-System

This project is a Python-based Face Recognition Attendance System that utilizes the [face_recognition](https://github.com/ageitgey/face_recognition) library to identify and record attendance of individuals in real-time using a webcam. It also integrates with Firebase for data storage and retrieval.

# Prerequisites
Before you start using the Face Recognition Attendance System, make sure you have the following prerequisites installed on your system:

- OpenCV (cv2) library
- face_recognition library
- Firebase Admin SDK

# Configuration
You can modify the following settings in the main.py script to customize the behavior of the system:

- cred: Path to your Firebase Admin SDK credentials file.
- databaseURL: URL of your Firebase Realtime Database.
- storageBucket: URL of your Firebase Storage bucket.
- imgBackground: Path to the background image displayed on the screen.
- folderModePath: Path to the directory containing different display modes.
- Other settings related to the display and behavior of the system.

# Acknowledgments
[face_recognition](https://github.com/ageitgey/face_recognition) library by Adam Geitgey.

