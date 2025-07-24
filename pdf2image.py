import fitz
import os

# In case if the user did not give the testing pdf in the first
# Might have chosen to prepare his own dataset 
def split_data_test(test_path):
    # Opens the pdf 
    pdf = fitz.open(test_path)

    # Goes through each page
    for i,page in enumerate(pdf):
        # converts each page into image
        img = page.get_pixmap(matrix = fitz.Matrix(1.5,1.5))
        # Update the save path and save the image
        save_path = test_path + f"-TESTING_page{i+1}.jpg"
        img.save(save_path)

# If the user wants to train the model with the labels he want to 
def split_data(pages_numbers,pdfs):
    

    # testing folder gets created only when he want to split the pages according to the test, val, train
    # If he did not enter the page numbers then testing folder can not be created so the user can give a new pdf to test without including the trained pdf
    if(pages_numbers is not None):
        if not os.path.exists("testing_data"):
            os.makedirs("testing_data")

    # If the training folder is not created 
    if not os.path.exists("training_data"):
        os.makedirs("training_data")
        os.makedirs("training_data\\train\\images")
        os.makedirs("training_data\\val\\images")

    # Goes through each pdf's if multiple
    for pd_num,pdf in enumerate(pdfs):
        # Opens the pdf 
        pdf = fitz.open(pdf)

        # Goes through each page in the selected pdf
        for i,page in enumerate(pdf):
            # converts each page into image
            img = page.get_pixmap(matrix = fitz.Matrix(1.5, 1.5))

            # Storing the paths
            test_path = "testing_data"
            train_path = "training_data\\train\\images"
            val_path = "training_data\\val\\images"

            # If "i" comes across the page_numbers entered by the user it stores them in the testing folder
            if pages_numbers is not None and  (i+1) in pages_numbers:
                test_path = test_path + f"\\PDF-{pd_num+1}-page{i+1}.jpg"
                img.save(test_path)
            else:
                # Spitting the validation data of every 10th page
                if((i+1)%10==0):
                    val_path = val_path + f"\\PDF-{pd_num+1}-page{i+1}.jpg"
                    img.save(val_path)
                else:
                # spitting the training data
                    train_path = train_path + f"\\PDF-{pd_num+1}-page{i+1}.jpg"
                    img.save(train_path)