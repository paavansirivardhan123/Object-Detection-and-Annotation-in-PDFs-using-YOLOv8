import annotation
import pdf2image
import model 
import os
import cv2
from pathlib import Path
from ultralytics import YOLO

# **WHEN USE WANTS TO MAKE HIS OWN DATASET AND TRAIN THE MODEL**
def prepare_your_model(pdfs):
    # The user can deploy the training data if he wants 
    # Either a single pdf of multiple pdf's
    pdf = pdfs 
    # If the user want to divide the testing data from the training data itself, he can manually enter the page numbers in the form of list
    # pages = [1,4,6,8,...etc]
    verify = int(input("Do you want to spilt me the testing pages or will you insert a testing pdf later[1/0]"))
    if(verify):
        # stores the numbers 
        pg_num = []
        # Loop does not brake until the user entered a non integer
        while True:
            val = input("Enter page number (once you are done enter a non integer): ")
            try:
                # Add the page number to the list for the further use 
                num = int(val)
                pg_num.append(num)
            
            # Not an integer 
            except ValueError:
                print("Non-integer input detected. Ending input.")
                break 
    else:
        # If the user wants to add the testing data later 
        pages = None
        pg_num =None

    pages = pg_num
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
    if not any(Path("testing_data//").glob("*.jpg")):
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
    for count,img in enumerate(sorted(img_path.glob("*.jpg"), key=lambda x: x.stat().st_mtime)):
        # As we are using the Pathlib library it displays in the formate of Windows() which need to be converted into String so our model can predict 
        results = custom_model.predict(source=str(img) , conf = 0.1,imgsz = 640)
        for result in results:
            # Save the images in the results folder
            cv2.imwrite(str(result_path / f"page{count+1}-result.jpg"), result.plot())


if __name__ =="__main__":
    # User can choose either the Per-trained or built a new model
    if int(eval(input("1 - > Use the pretrained model\n0 - > Prepare your own model\nENTER EITHER [1/0]")))==1:
        pretrained_model()
    else:
        # Create a pdf's folder to store the pdf's 
        if not os.path.exists("pdf's"):
            os.makedirs("pdf's")
        # Stores the pdf paths 
        pdfs_paths = []
        # If the length of the pdf's folder is Zero then he didn't place his pdf's in it
        # Loops until the folder has at least 1 pdf in it
        while(len(pdfs_paths)==0):
            # The is display message
            print("The pdf's folder is empty, enter at least 1 pdf in it ")
            # For conformation
            verify = int(input("Did you enter[1/0]: "))
            # If user entered the pdf's in it then add them to the pdf_path so we can easily annotate them
            if(verify):

                pdfs = Path("pdf's")
                

                for pdf in pdfs.glob("*.pdf"):
                    # covert them into string 
                    pdfs_paths.append(str(pdf))
            
        print(len(pdfs_paths))
        prepare_your_model(pdfs_paths)