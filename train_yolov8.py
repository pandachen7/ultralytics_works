import os

from ultralytics import YOLO

home_dir = os.path.expanduser("~")

## choose one model of [yolov8n, yolov8s, yolov8m, yolov8l, yolov8x]
model = YOLO("yolov8l.yaml")

metrics = model.train(
            data=f"{home_dir}/datasets/rpi4_model_b_plus_video.v2i.yolov8/data.yaml",
            mode="detect",
            epochs=1000,
            batch=16,
            imgsz=640,
            save=True,
            save_period=50,
            device="0",
            exist_ok=True,
            close_mosaic=0,
            plots=True)

print("training res:")
print(f"map50-95(B): {metrics.box.map}, map50(B): {metrics.box.map50}")
print(f"map75(B): {metrics.box.map75}, a list contains map50-95(B) of each category: {metrics.box.maps}")