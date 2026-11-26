# People Tracking & Counting

A real-time video analytics experiment that detects and tracks people with **Ultralytics YOLO** and **OpenCV**, then counts unique tracked people crossing a configured horizontal line.

The application reads a video file, detects the person class, and uses the bottom-center point of each bounding box as the crossing reference. A person is counted only when the interpolated crossing point falls within the visible line segment.

## Features

- Person detection with the local `yolo11n.pt` model
- Persistent object tracking between video frames
- Per-track ID handling
- One-direction line-crossing count (top to bottom)
- Crossing validation against the visible line segment
- Duplicate count prevention for IDs already counted
- Bounding-box and foot-point visualization
- Live count and counting-line overlay
- Unit tests for line-crossing edge cases
- Custom BoT-SORT configuration file included for future tracker tuning

## Project structure

```text
people-tracking/
├── counting_line.py       # Isolated line-crossing logic
├── main.py                # Video processing, tracking, and counting
├── tests/
│   └── test_counting_line.py
├── yolo11n.pt              # YOLO11 nano model weights
├── botsort_custom.yaml     # Custom BoT-SORT settings (not currently passed by main.py)
├── requirements.txt        # Python dependencies
└── videos/
    └── input.mp4           # Default input video
```

## Requirements

- Python
- A working desktop environment for the OpenCV preview window

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

## Run

From the repository root:

```bash
python main.py
```

The script opens `videos/input.mp4`, loads `yolo11n.pt`, and displays a window named **Video**. Press **Q** while the preview window is focused to stop processing.

To use another video, update the `cv2.VideoCapture("videos/input.mp4")` path in `main.py`.

## Automated tests

The line-crossing function is kept in a small standalone module so it can be tested without loading the YOLO model or opening a webcam.

Run the tests with Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests -v
```

The test suite covers valid vertical and diagonal crossings, both line endpoints, crossings outside the visible segment, upward movement, and movement that does not cross the line.

## Counting logic

1. YOLO runs tracking on each frame with persistent track IDs.
2. Detections whose class ID is not `0` are ignored (class `0` is the person class in the included YOLO model).
3. The bottom-center point of each person's bounding box is used as the reference point.
4. When a tracked point moves from above the line to the line or below it, the code interpolates its X coordinate at the crossing moment.
5. The crossing is counted only when that interpolated X coordinate falls between the line endpoints, currently `600` and `1000`.
6. Each track ID is counted at most once during a run.

The counting line is drawn from `(600, 500)` to `(1000, 500)`. The current implementation counts top-to-bottom crossings only.

## Configuration and limitations

- The input path, model path, and counting-line coordinates are currently hard-coded.
- The included `botsort_custom.yaml` is not currently supplied to `model.track()`; the script therefore uses the tracker default selected by the installed Ultralytics version.
- Counts depend on stable tracking IDs. Occlusion, crowded scenes, fast movement, or tracker ID switches can affect results.
- The current logic does not count people moving in the opposite direction.
- The script keeps counted IDs in memory and resets the count each time it is started.
- The project is an experimental video analytics demo, not a validated people-counting system.

## Next improvements

- Make the video, model, and line coordinates configurable
- Support both entry and exit directions
- Export timestamped counting events to CSV
- Add command-line options
- Add end-to-end tests using short sample videos
