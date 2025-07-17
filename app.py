import annotation
import pdf2image
import model 
import os
import cv2
from pathlib import Path
from ultralytics import YOLO

pdf = ["infosys-2022.pdf","infosys-2023.pdf","infosys-2024.pdf","infosys-2025.pdf", "TCS_2023", "TCS_2024"]


pages = None
print(len(pages))

pdf2image.split_data(pages, pdf)
annotation.main()

epoch = int(input("Enter the no of epochs"))
custom_model = model.load_train_the_model(epoch)

# custom_model = YOLO("trained_model/custom_model/weights/best.pt")

pdf_name = ""
while True:
    if not os.path.exists("testing_data"):
        os.makedirs("testing_data")
        
    print("Share/Place your PDF for the predictions in the testing_data folder")

    if int(eval(input("Did you place the pdf in the folder [1/0]")))!=0:
        if pdf_name =="":
            pdf_name = input("Place the PDF and enter the name:")
        pdf2image.split_data_test(f"testing_data\\{pdf_name}")
        break
    else:
        pdf_name = input("Place the PDF and enter the name:")



img_path = Path("testing_data\\")
result_path = Path("results\\")

if not os.path.exists(str(result_path)):
    os.makedirs(str(result_path))

count =1 
for img in img_path.glob("*.jpg"):
    results = custom_model.predict(source=str(img) , conf = 0.1,imgsz = 640)
    for result in results:
        conf = result.boxes.conf.squeeze()
        idx = (conf > 0.5).nonzero(as_tuple=True)[0]

        if len(idx):
            result.boxes = result.boxes[idx]
            cv2.imwrite(str(result_path / f"result{count}.jpg"), result.plot())
            count += 1
        else:
            print("No Detection")
    