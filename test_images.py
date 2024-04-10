import os

from ultralytics import YOLO

home_dir = os.path.expanduser("~")

model = YOLO(f"./runs/detect/train/weights/epoch350.pt")

result = model.predict(
    source=f"{home_dir}/dataset/raw_rpi",
    conf=0.25,
    iou=0.5,
    device="cpu",
    # agnostic_nms=True,

    save=True,
    mode="predict",
)