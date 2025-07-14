import fitz
import os

def split_data(pages_numbers,pdf_path):

    #testing folder
    if not os.path.exists("testing_data"):
        os.makedirs("testing_data")

    # training folder / images
    if not os.path.exists("training_data"):
        os.makedirs("training_data")

    if not os.path.exists("training_data\\images"):
        os.makedirs("training_data\\images")

    pdf = fitz.open(pdf_path)

    for i,page in enumerate(pdf):
        img = page.get_pixmap(dpi = 300)
        path = f"testing_data\\page{i+1}.jpg"
        

        if pages_numbers != "all":
            if i+1 in pages_numbers:
                test_path = f"training_data\\images\\page{i+1}.jpg"
                img.save(test_path)
            else:
                img.save(path)
        else:
            test_path = f"training_data\\images\\page{i+1}.jpg"
            img.save(test_path)
