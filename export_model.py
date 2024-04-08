from ultralytics import YOLO

model = YOLO('./runs/detect/train31/weights/last.pt')

success = model.export(format='onnx')
