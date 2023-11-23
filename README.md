# Driver Caution Project

## Introduction

This project is designed to detect if a driver is falling asleep and alert them. It uses face mesh detection to monitor the driver's eyes and plays a beep sound if the driver appears to be falling asleep.

## Dependencies

This project requires the following dependencies:

- Python
- OpenCV
- MediaPipe
- Pygame

You can install these dependencies using pip:

```bash
# Update pip to the latest version
python -m pip install --upgrade pip

# Install OpenCV
pip install opencv-python

# Install MediaPipe
pip install mediapipe

# Install Pygame
pip install pygame
```

## Files

- driver_caution.py: This is the main script that runs the detection and alert system.
- beep.wav: This is the sound file that is played when the driver is detected to be sleepy.

## How to Run

1. Install the required dependencies.
2. Run the driver_caution.py script.

## Code Explanation

The script loads the beep sound using Pygame's mixer. It then sets up the face mesh detection using MediaPipe's drawing utilities and face mesh solution.

The alert function plays the beep sound if it's not already playing.

The landmarkToPoint function converts a landmark (a point on the face mesh) to a point with x, y, and z coordinates.

## Deployment

This script can be deployed on any system with a camera, Python, and the required dependencies installed. It could be used in a real-world setting to help prevent accidents caused by drivers falling asleep at the wheel.

## Contributing
Contributions to the `Driver conscious caution system` project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

