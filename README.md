# Visual-Presentation-ML-OpenCV-Project
## Hand Gesture Controlled Presentation

This project demonstrates a hand gesture controlled presentation application using computer vision techniques. It allows users to navigate through a series of slides by detecting hand gestures captured through the webcam.

## Features

- Slide navigation using hand gestures:
  - Show the next slide by extending the index finger.
  - Show the previous slide by making a fist with the hand.
- Drawing annotations on slides using the index finger:
  - Start drawing annotations by closing the thumb and extending the index finger.
  - Erase the last annotation by extending the thumb, index finger, and middle finger simultaneously.

## Requirements

- Python 3.x
- OpenCV (cv2) library
- cvzone library
- NumPy library

## Setup and Usage

1. Clone the repository or download the project files.
2. Install the required libraries using pip:
```
pip install opencv-python
pip install cvzone
pip install numpy
```
3. Place your presentation images in the "Presentation" folder. Rename them in a sequential manner for proper slide navigation.
4. Run the `main.py` script:
```python main.py```
5. Ensure that your webcam is working and properly detected by the script.
6. Use the defined hand gestures to navigate through slides and draw annotations as described in the Features section.

## Demo

![Demo](demo.gif)

## Acknowledgments

This project utilizes the `cvzone` library, created by [Murtaza Hassan](https://github.com/murtazahassan).

## License

This project is licensed under the [MIT License](LICENSE).
