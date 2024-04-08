from ultralytics import YOLO
from pathlib import Path

# PATH_DATESET = "D:/datasets/Test.v1i.yolov8"

PATH_DATESET = "D:/datasets/train_liyu_lake_2020_10"

if __name__ == "__main__":
    model = YOLO("yolov8m.pt")

    model.train(data=f"{PATH_DATESET}/data.yaml", epochs=1000, imgsz=640, device="0")
    # results = model.train(data="coco128.yaml", epochs=1000, imgsz=640, device=0)
