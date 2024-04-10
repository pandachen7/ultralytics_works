import os

from ultralytics import YOLO

home_dir = os.path.expanduser("~")

model = YOLO(f"./runs/detect/train/weights/epoch350.pt")

result = model.predict(
    source=f"./record/rpi4_pixel4a.mp4",
    conf=0.25,
    iou=0.5,
    device="0",
    # agnostic_nms=True,

    save=True,
    mode="predict",
)