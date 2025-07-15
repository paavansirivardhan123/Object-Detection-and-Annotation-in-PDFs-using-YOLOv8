import fitz
import os

def split_data(pages_numbers,pdf_path):

    # testing folder
    if not os.path.exists("testing_data"):
        os.makedirs("testing_data")

    # training folder / images
    if not os.path.exists("training_data"):
        os.makedirs("training_data")
        os.makedirs("training_data\\train\\images")
        os.makedirs("training_data\\val\\images")

    pdf = fitz.open(pdf_path)

    for i,page in enumerate(pdf):
        img = page.get_pixmap(matrix = fitz.Matrix(1.5, 1.5))
        test_path = "testing_data"
        train_path = "training_data\\train\\images"
        val_path = "training_data\\val\\images"

        if i+1 in pages_numbers:
            test_path = test_path + f"\\image{i+1}.jpg"
            img.save(test_path)
        else:
            if((i+1)%10==0):
                val_path = val_path + f"\\image{i+1}.jpg"
                img.save(val_path)
            else:
                train_path = train_path + f"\\image{i+1}.jpg"
                img.save(train_path)