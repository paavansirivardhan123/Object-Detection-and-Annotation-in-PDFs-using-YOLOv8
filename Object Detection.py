import annotation
import pdf2image
import model 
import os
import cv2
from pathlib import Path
from ultralytics import YOLO

# **WHEN USE WANTS TO MAKE HIS OWN DATASET AND TRAIN THE MODEL**
def prepare_your_model():
    # The user can deploy the training data if he wants 
    # Either a single pdf of multiple pdf's
    pdf = ["infosys-2022.pdf","infosys-2023.pdf","infosys-2024.pdf","infosys-2025.pdf", "TCS_2023.pdf", "TCS_2024.pdf"]

    # If the user want to divide the testing data from the training data itself, he can manually enter the page numbers in the form of list
    # pages = [1,4,6,8,...etc]
    pages = None

    # This function is used to convert  the pdf into images(page by page)
    # split them into training, validation and testing automatically it creates the folders
    # converting the data to images helps us in annotation and for the model training  
    pdf2image.split_data(pages, pdf)

    # Opens a GUI(Graphical User Interface) 
    # The converted images are going to be seen one by one so we do the annotation smoothly
    annotation.main()

    # If the number of epochs are fixed, It may take a long time to train the model if the user has low ram 
    # To avoid the inconvenience user has a free will to choose the number of epochs 
    # Suggested epochs with respective ram if the over all images are greater than 1200
    # 2 GB - epochs 10 to 15
    # 4 GB – epochs 20 to 35
    # 8 GB – epochs 30 to 50
    # 16 GB – epochs > 75
    epoch = int(input("How many training approaches do you want to run?"))

    # In this function the model training is going to be done considering the labels which you have mentioned
    custom_model = model.load_train_the_model(epoch)
    pretrained_model(custom_model)

## **IN CASE IF THE USER DOES WANT TO PREPARE HIS OWN DATASET OR ANNOTATE THE IMAGES**
def pretrained_model(custom_model = YOLO("pretrained_model.pt")):
    # here is the pre trained model which can predict the [text,image,table] in the pdf 
    # The the user must have the pretrained model

    pdf_name = ""
    # Using a while loop so the the predictions only preform when the user places his testing pdf in the testing_data folder
    while True:
        # If the testing folder is not yet created by the user it does automatically
        if not os.path.exists("testing_data"):
            os.makedirs("testing_data")
        
        # Requesting the user to place the pdf 
        print("Place your PDF for the predictions in the testing_data folder")

        # Asking the pdf name to the user to for the easy access 
        pdf_name = input("Place the PDF and enter the correct name with extension(.pdf):")

        # Using eval to avoid the any spaces
        if int(eval(input("Did you place the pdf in the folder [1/0]")))!=0:
            # Make sure that the user should enter the pdf name or else it will not preform the convert them into images
            if pdf_name =="":
                pdf_name = input("Place the PDF and enter the name:")
            else:
                pdf2image.split_data_test(f"testing_data\\{pdf_name.lower()}")
                break
            

    # To access the images 
    img_path = Path("testing_data\\")

    # To store the results
    result_path = Path("results\\")
    # If not exists create one
    if not os.path.exists(str(result_path)):
        os.makedirs(str(result_path))


    # Only filter the files which ends with .jpg
    for count,img in enumerate(img_path.glob("*.jpg")):
        # As we are using the Pathlib library it displays in the formate of Windows() which need to be converted into String so our model can predict 
        results = custom_model.predict(source=str(img) , conf = 0.1,imgsz = 640)
        for result in results:
            # Save the images in the results folder
            cv2.imwrite(str(result_path / f"page{count+1}-result.jpg"), result.plot())


if __name__ =="__main__":
    if int(eval(input("1 - > Use the pretrained model\n0 - > Prepare your own model\nENTER EITHER [1/0]")))==1:
        pretrained_model()
    else:
        prepare_your_model()