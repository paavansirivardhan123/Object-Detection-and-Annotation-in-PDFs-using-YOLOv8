import fitz
import os


def split_data_test(test_path):
    pdf = fitz.open(test_path)
    for i,page in enumerate(pdf):
        img = page.get_pixmap(matrix = fitz.Matrix(1.5,1.5))
        save_path = test_path + f"-TESTING_image{i+1}.jpg"
        img.save(save_path)


def split_data(pages_numbers,pdfs):
    

    # testing folder
    if(pages_numbers is not None):
        if not os.path.exists("testing_data"):
            os.makedirs("testing_data")

    # training folder / images
    if not os.path.exists("training_data"):
        os.makedirs("training_data")
        os.makedirs("training_data\\train\\images")
        os.makedirs("training_data\\val\\images")

    for pd_num,pdf in enumerate(pdfs):
        pdf = fitz.open(pdf)

        for i,page in enumerate(pdf):
            img = page.get_pixmap(matrix = fitz.Matrix(1.5, 1.5))
            test_path = "testing_data"
            train_path = "training_data\\train\\images"
            val_path = "training_data\\val\\images"

            if pages_numbers is not None and  (i+1) in pages_numbers:
                test_path = test_path + f"\\PDF-{pd_num+1}-image{i+1}.jpg"
                img.save(test_path)
            else:
                if((i+1)%10==0):
                    val_path = val_path + f"\\PDF-{pd_num+1}-image{i+1}.jpg"
                    img.save(val_path)
                else:
                    train_path = train_path + f"\\PDF-{pd_num+1}-image{i+1}.jpg"
                    img.save(train_path)