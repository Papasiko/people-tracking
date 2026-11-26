import cv2
from ultralytics import YOLO

LINE_START = (600, 500)
LINE_END = (1000, 500)
LINE_Y = LINE_START[1]


def crosses_counting_line(previous_position, current_position):
    """Return whether a tracked foot point crosses the visible line top-to-bottom."""
    previous_x, previous_y = previous_position
    current_x, current_y = current_position

    if not (previous_y < LINE_Y <= current_y):
        return False

    delta_y = current_y - previous_y
    if delta_y == 0:
        return False

    # Interpolate the X coordinate at the exact frame-to-frame crossing point.
    crossing_ratio = (LINE_Y - previous_y) / delta_y
    crossing_x = previous_x + crossing_ratio * (current_x - previous_x)

    return LINE_START[0] <= crossing_x <= LINE_END[0]


cap = cv2.VideoCapture("videos/input.mp4")
model = YOLO("yolo11n.pt")
count = 0
counted_ids = set()
last_positions = {}

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model.track(frame, persist=True, verbose=False)

    for box in results[0].boxes:
        cls = int(box.cls[0])

        if cls != 0:
            continue

        if box.id is None:
            continue

        track_id = int(box.id[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        foot_x = (x1 + x2) // 2
        foot_y = y2

        previous_position = last_positions.get(track_id)

        print(f"ID:{track_id}")

        if previous_position is not None and track_id not in counted_ids:
            if crosses_counting_line(previous_position, (foot_x, foot_y)):
                counted_ids.add(track_id)
                count += 1

        last_positions[track_id] = (foot_x, foot_y)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )
        cv2.circle(
            frame,
            (foot_x, foot_y),
            5,
            (255, 0, 0),
            -1
        )

    cv2.putText(
        frame,
        f"Count: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.line(
        frame,
        LINE_START,
        LINE_END,
        (0, 0, 255),
        3
    )

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
