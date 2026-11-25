# People Tracking & Counting

A real-time video analytics experiment that detects and tracks people with **Ultralytics YOLO** and **OpenCV**, then counts unique tracked people crossing a configured horizontal line.

The current script reads a video file, detects only the person class, uses each bounding box's bottom-center point as the crossing reference, and increments the count when a tracked ID moves from above the line to the line or below it.

## Features

- Person detection with the local `yolo11n.pt` model
- Persistent object tracking between video frames
- Per-track ID handling
- One-direction line-crossing count (top to bottom)
- Duplicate count prevention for IDs already counted
- Bounding-box and foot-point visualization
- Live count and counting-line overlay
- Custom BoT-SORT configuration file included for future tracker tuning

## Project structure

```text
people-tracking/
├── main.py              # Video processing, tracking, and line-crossing count
├── yolo11n.pt           # YOLO11 nano model weights
├── botsort_custom.yaml  # Custom BoT-SORT settings (not currently passed by main.py)
├── requirements.txt     # Python dependencies
└── videos/
    └── input.mp4        # Default input video
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

## Counting logic

1. YOLO runs tracking on each frame with persistent track IDs.
2. Detections whose class ID is not `0` are ignored (class `0` is the person class in the included YOLO model).
3. The bottom-center point of each person's bounding box is used as the reference point.
4. A person is counted when that point moves from a Y coordinate below `500` in the previous frame to a Y coordinate of `500` or greater in the current frame.
5. Each track ID is counted at most once during a run.

The counting line is currently drawn from `(600, 500)` to `(1000, 500)`. The crossing test uses the Y coordinate only, so it does not currently restrict counting to the visible line segment's X range.

## Configuration and limitations

- The input path, model path, and counting-line coordinates are currently hard-coded in `main.py`.
- The included `botsort_custom.yaml` is not currently supplied to `model.track()`; the script therefore uses the tracker default selected by the installed Ultralytics version.
- Counts depend on stable tracking IDs. Occlusion, crowded scenes, fast movement, or tracker ID switches can affect results.
- The current logic counts only top-to-bottom crossings and does not count people moving in the opposite direction.
- The script keeps counted IDs in memory and resets the count each time it is started.
- The project is an experimental video analytics demo, not a validated people-counting system.

## Next improvements

- Make the video, model, and line coordinates configurable
- Restrict crossing checks to a finite line segment
- Support both entry and exit directions
- Export timestamped counting events to CSV
- Add command-line options and automated tests
