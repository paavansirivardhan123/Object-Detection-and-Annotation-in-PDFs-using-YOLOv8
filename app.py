import annotation
import pdf2image
import model 
import os
import cv2
from pathlib import Path

pdf = "pdf.pdf"

pdf2image.split_data([1,4,6,8,10], pdf)
annotation.main()

custom_model = model.load_train_the_model()

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