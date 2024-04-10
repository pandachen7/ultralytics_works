import os

from ultralytics import YOLO

home_dir = os.path.expanduser("~")

## choose one model of [yolov8n, yolov8s, yolov8m, yolov8l, yolov8x]
model = YOLO("yolov8l.yaml")

model.train(data=f"{home_dir}/datasets/Test.v1i.yolov8/data.yaml",
            mode="detect",
            epochs=1000,
            batch=8,
            imgsz=640,
            save=True,
            save_period=50,
            device="0",
            exist_ok=True,
            close_mosaic=0,
            plots=True)
