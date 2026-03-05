import os

from ultralytics import YOLO

# 設定你的yaml設定檔路徑
home_dir = os.path.expanduser("~")
data_config = f"{home_dir}/datasets/data.yaml"

# choose one model of [yolo26n, yolo26s, yolo26m, yolo26l, yolo26x]
model = YOLO("yolo26l.yaml")

metrics = model.train(
    data=data_config,
    mode="detect",
    epochs=1000,
    batch=16,  # 太高導致OOM就調低
    imgsz=640,
    save=True,
    save_period=50,
    device="0",
    exist_ok=True,
    close_mosaic=0,
    plots=True,
)

print("training res:")
print(f"map50-95(B): {metrics.box.map}, map50(B): {metrics.box.map50}")
print(
    f"map75(B): {metrics.box.map75}, a list contains map50-95(B) of each category: {metrics.box.maps}"
)
