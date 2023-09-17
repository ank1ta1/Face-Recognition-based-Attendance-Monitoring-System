# Face-Recognition-based-Attendance-Monitoring-System

This project is a Python-based Face Recognition Attendance System that utilizes the face_recognition library to identify and record attendance of individuals in real-time using a webcam. It also integrates with Firebase for data storage and retrieval.

# Prerequisites
Before you start using the Face Recognition Attendance System, make sure you have the following prerequisites installed on your system:

Python 3.x\n
OpenCV (cv2) library\n
face_recognition library\n
Firebase Admin SDK\n
NumPy\n

# Configuration
You can modify the following settings in the main.py script to customize the behavior of the system:

cred: Path to your Firebase Admin SDK credentials file.\n
databaseURL: URL of your Firebase Realtime Database.\n
storageBucket: URL of your Firebase Storage bucket.\n
capt.set(3, 640): Width of the captured video frame.\n
capt.set(4, 480): Height of the captured video frame.\n
imgBackground: Path to the background image displayed on the screen.\n
folderModePath: Path to the directory containing different display modes.\n
modetype: Default mode for displaying information.\n
Other settings related to the display and behavior of the system.\n

# Acknowledgments
face_recognition library by Adam Geitgey.

