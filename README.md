# Red Line Tracking for Autonomous Underwater Vehicle (AUV)

This project implements a real-time red line tracking system for an Autonomous Underwater Vehicle (AUV) using OpenCV and Python. The system processes video frames, detects red lines, calculates their center positions, and generates control commands for the AUV based on the detected position.

## Features
- Detects red lines in a video feed using HSV color space.
- Applies Gaussian blur for noise reduction.
- Identifies the largest detected red contour and calculates its center.
- Generates control commands for the AUV to move forward, turn left, or turn right based on the red line's position.
- Displays real-time processed video frames and the red mask.

## Installation
Ensure you have Python installed, then install the required dependencies:
```sh
pip install opencv-python numpy
```

## Usage
Run the script to start the video processing and red line tracking:
```sh
python auv_red_line_tracking.py
```
Press `q` to exit the program.

## Code Overview
### `process_frame(frame)`
- Converts the frame to HSV color space.
- Creates a mask for red color detection.
- Applies Gaussian blur to smooth the mask.
- Finds contours and identifies the largest red object.
- Calculates the center of the detected red line.

### `control_auv(cx, frame_width)`
- Determines the AUV's movement based on the red line's position.
- Commands:
  - **"FORWARD"** if the red line is centered.
  - **"TURN LEFT"** if the red line is towards the left.
  - **"TURN RIGHT"** if the red line is towards the right.
  - **"STOP"** if no red line is detected.

### `main()`
- Captures video from the camera.
- Processes each frame and determines control commands.
- Displays the processed video frames and control commands.
- Listens for user input to exit the program.

## Controls
- Press `q` to exit the program.
