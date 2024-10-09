# Hand and Arm Tracking with MediaPipe, OpenCV, and Arduino

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Servo Motor Mapping](#servo-motor-mapping)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
This project enables real-time tracking of hand and arm positions using MediaPipe and OpenCV, sending data to an Arduino using pyFirmata to control servo motors. It's ideal for applications like robotics, prosthetics, and gesture-controlled devices.

## Features
- Real-time pose estimation of the arm (shoulder, elbow, wrist)
- Control multiple servo motors based on arm angles
- Visualization of detected angles in the live video feed
- Easy-to-use setup with an Arduino and Python

## Requirements
| Software  | Version |
|-----------|---------|
| Python    | 3.x     |
| OpenCV    | Latest  |
| MediaPipe | Latest  |
| NumPy     | Latest  |
| PyFirmata | Latest  |

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hand_tracking_using-mediapipe_opencv.git
   cd hand_tracking_using-mediapipe_opencv
2. **Install dependencies:**

   bash
   Copy code
   **pip install opencv-python mediapipe numpy pyfirmata**
   
3.  **Upload Arduino sketch:**

Ensure your Arduino is flashed with the pyfirmata sketch for controlling servos.

# Configure the serial port:

In the Python script, modify the port variable to the correct port where your Arduino is connected:

**Linux: /dev/ttyACM0
Windows: COM3**

# Usage
Connect your webcam (or use a built-in camera).
Run the following command to start the program:
# bash
Copy code
**python track_that_arm.py**
