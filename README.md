# Virtual Hover Pen

A real-time hand gesture drawing application that lets you paint on a virtual canvas using your webcam and bare hands. No mouse or touchscreen required.

---

## Overview

Virtual Hover Pen uses computer vision to track your hand landmarks through the webcam and translates finger movements into brush strokes on a black canvas. The brush size adjusts dynamically based on the distance between your thumb and index finger.

---

## Project Structure

```
Virtual-Hover-Pen-master/
│
├── test.py                  # Main application code
├── requirements.txt         # Python dependencies
└── screenshots/             # Saved canvas screenshots (auto-created)
```

---

## Requirements

- Python 3.7 or above
- Webcam

### Dependencies

```
opencv-python
mediapipe
numpy
```

---

## Installation

1. Clone the repository or download the project folder.

2. Navigate to the project directory:
   ```bash
   cd Virtual-Hover-Pen-master
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

```bash
python test.py
```

Two windows will open: one showing the webcam feed with hand landmarks, and one showing the drawing canvas.

---

## Controls

| Action | Control |
|---|---|
| Draw | Raise index finger and move hand |
| Save canvas | Thumbs up gesture (2 second cooldown) |
| Save canvas manually | Press P |
| Switch to Red | Press R |
| Switch to Green | Press G |
| Switch to Blue | Press B |
| Switch to Yellow | Press Y |
| Eraser mode | Press E |
| Clear canvas | Press C |
| Toggle instructions | Press H |
| Quit | Press Esc |

---

## How Drawing Works

- Raising your index finger activates freehand drawing.
- The brush thickness is controlled by the distance between your thumb tip and index finger tip. Pinch closer for a thin brush, spread wider for a thick brush.
- Lowering your index finger pauses drawing.
- A thumbs up gesture automatically saves the current canvas as a PNG file in the `screenshots/` folder.

---

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
