from ultralytics import YOLO
import cv2 
from pathlib import Path
import os

model = YOLO("yolov8n.pt")

model.train(
    data="data.yaml",
    epochs=10,
    imgsz=640,
    project="trained_model",   
    name="custom_model",       
    exist_ok=True          
)

custom_model = YOLO("trained_model/custom_model/weights/best.pt")

img_path = Path("testing_data\\")
result_path = Path("results\\")

if not os.path.exists(str(result_path)):
    os.makedirs(str(result_path))

count =1 

for img in img_path.glob("*.jpg"):
    results = custom_model.predict(source=str(img) , conf = 0.1,imgsz = 640)
    for result in results:
        boxes = result.boxes
        if boxes and boxes.xyxy.numel()>0:
            output_file = result_path / f"result{count}.jpg"
            cv2.imwrite(output_file, result.plot())
            count+=1
        else:
            print("No Detection")
