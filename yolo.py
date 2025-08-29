from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="custom.yaml",
    epochs=200,
    batch=32,
    imgsz=640,
    device="cuda"
)

