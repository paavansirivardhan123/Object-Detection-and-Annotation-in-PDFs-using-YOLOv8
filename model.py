from ultralytics import YOLO
import cv2 
from pathlib import Path
import os

def load_train_the_model():
    model = YOLO("yolov8n.pt")

    model.train(
        data="data.yaml",
        epochs=2,
        imgsz=640,
        project="trained_model",   
        name="custom_model",       
        exist_ok=True          
    )

    custom_model = YOLO("trained_model/custom_model/weights/best.pt")

    return custom_model