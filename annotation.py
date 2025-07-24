import cv2
from pathlib import Path

# Created the Globals Variables for the easy flow among the functions 
# Helps in reduce the params pass again and again 
annotations = []
drawing = False
label_input_mode = False
current_label = ""
ix, iy = -1, -1
curr_x, curr_y = -1, -1
box_coords = None

# Only works when the mouse is in the GUI window 
# The activities are recoded when the mouse is performing any activity  
# This function requires 5 in those we use 3 they are event, x,y
# event states that the operation performed on the mouse 
# x, y are the mouse Coordinates when an event occurred
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, curr_x, curr_y, box_coords, label_input_mode, current_label
    
    # Works when we press the Left click
    # It records the positions of the leftdown and enables the drawing which helps in the real time drawing 
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        curr_x, curr_y = x, y

    # Only works when the drawing is True so we can see the rectangle is fixed to the start point
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # continuously reads the coordinates which helps in the real time monitoring 
            curr_x, curr_y = x, y
        
    # Works when we realize the left button
    # That means the drawing is completed now we need to add the label name for the selected area 
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # current x, y values becomes the endpoints of the rectangle 
        curr_x, curr_y = x, y
        # Store the values for further use 
        box_coords = (ix, iy, curr_x, curr_y)
        label_input_mode = True
        current_label = ""

def annotate_image(image_path):
    global img, annotations, label_input_mode, current_label, box_coords, drawing

    annotations = []

    # Read the image in the image path and store it in the img
    img = cv2.imread(image_path)
    # storing the original image for the later use 
    clone = img.copy()
    
    # You can change according to you computer resolution 
    screen_w = 1280
    screen_h = 960

    # The img.shape returns the (height, width, channel)
    # We use only the height and width 
    img_h, img_w = img.shape[:2]

    # Check whether the img can fit in the computer screen or not 
    # If the image width or the image height are grater then the screen the we need the adjust that
    # By scale it horizontally or vertically
    # we are taking the minimum because neither the width nor the height exceeds the screen
    scale = min(screen_w / img_w , screen_h / img_h , 1.0)

    # If it is 1 then it can fit in the screen
    # No need of resizing the image 
    if scale < 1.0:
        # resize mean it is enlarge or shrink the image not to crop the image 
        # resize the image according to the scale
        # Multiplying the min scale with the img_w and img_h can helps the img to fit in the screen
        img = cv2.resize(img, (int(img_w * scale), int(img_h * scale)))

        # copy the resized image 
        clone = img.copy()

    # We use auto size so to avoid the fixed size of GUI which is very useful for different sizes
    cv2.namedWindow("Annotator", cv2.WINDOW_AUTOSIZE)

    # Helps in track of the mouse activities
    # This function works on the GUI window until the window is closed, Give a live tracking effect
    # Then the draw_rectangle function invoke
    cv2.setMouseCallback("Annotator", draw_rectangle)

    while True:
        # Not to make any changes until we are conform about it so we store them in a variable
        display_img = img.copy()

        # For real time only works when we click the left button
        if drawing:
            cv2.rectangle(display_img, (ix, iy), (curr_x, curr_y), (0, 255, 255), 2)

        # To add label to the selected area when we realize the left button
        if label_input_mode:
            # Helps to see the label we entered 
            cv2.putText(display_img, f"Label: {current_label}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # show the image were changes are made 
        cv2.imshow("Annotator", display_img)

        key = cv2.waitKey(1) & 0xFF

        # Works when left button is realized
        if label_input_mode:

            # Works only for enter key windows is 13 and for Linux is 10
            if key == 13 or key == 10: 
                # Adds to the annotations list
                annotations.append({
                    "label": current_label,
                    "box": list(box_coords)
                }) 

                # Now we can make the change in the original image 
                # Draws a rectangle
                cv2.rectangle(img, (box_coords[0], box_coords[1]), (box_coords[2], box_coords[3]), (0, 255, 0), 2)

                # Helps to label the name the on the box
                cv2.putText(img, current_label, (box_coords[0], box_coords[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                # Not to fall in a label_input_mode loop
                label_input_mode = False
                box_coords = None
                current_label = ""

            # Used for the backspacing 
            elif key == 8: 
                current_label = current_label[:-1]
            # Used to the alphabets 
            # ASCII value of 32 is 'a' and 126 is 'Z'
            elif 32 <= key <= 126: 
                current_label += chr(key)   
            continue
        
        # Reset the edited image
        if key == ord("r"):
            # clone is used here 
            img = clone.copy()
            # Make sure none edits so no annotations
            annotations = []
        # q means close the window 
        # If multiple images it automatically opens the next image 
        elif key == ord("q"):
            break
    
    # Used to close all GUI windows 
    cv2.destroyAllWindows()

    return annotations, img

def process_images(image_dir, label_dir, classes):
    # OS for easy storing of the data
    import os 

    # Creates the label folders if not exists
    os.makedirs(label_dir, exist_ok=True)

    # Go through every image and stores the image paths and return a list 
    image_paths = list(Path(image_dir).glob("*.jpg"))

    # Goes through each image 
    for image_path in image_paths:
        # main function for the image annotation 
        # We send the image path to the function 
        annotations, img = annotate_image(str(image_path))  

        
        h, w = img.shape[:2] 
        # For storing the boxes in the image 
        boxes = []

        # Goes through every annotation made in the image 
        for ann in annotations:
            # Store the label name in the label 
            label = ann["label"]

            # Get the box of that particular label in that image 
            box = ann["box"]

            # If the user entered a new label then add that to the classes variable 
            # Will be useful in for the data.yaml
            if label not in classes:
                classes.append(label)
            # Returns the index
            class_index = classes.index(label)

            # stores the values of the start(x,y) and end(x,y)
            x1, y1, x2, y2 = box

            # convert them into the YOLO model format so that our model can understand
            x_center = (x1 + x2) / 2 / w
            y_center = (y1 + y2) / 2 / h
            width = abs(x2 - x1) / w
            height = abs(y2 - y1) / h

            # Well formatted so that the model can understand 
            boxes.append((class_index, x_center, y_center, width, height))

        # Create a new label for that image 
        label_save_path = os.path.join(label_dir, f"{image_path.stem}.txt")

        with open(label_save_path, "w") as f:
            # All the boxes in that image
            for box in boxes:
                class_id, x_center, y_center, width, height = box

                # Not a proper box
                if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and width > 0 and height > 0):
                    continue

                # Well formatted so that the model can understand 
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


# Calls from the Object detection.py
def main():
    # Helps in creating the data.yaml file of the model training 
    import yaml
    # To store the unique labels the user entered while annotating the image 
    classes = []
    
    # Function helps in the annotation part
    # we pass the images path, labels path (where the label_index, boxes are stored), classes
    # Create labels for the training images
    process_images("training_data/train/images", "training_data/train/labels", classes)
    
    # Create labels for the validation images
    process_images("training_data/val/images", "training_data/val/labels", classes)

    # After creating the labels 
    # We need to keep a track class file to access the number of classes 
    # Also helps in the data.yaml 
    with open("classes.txt", "w") as f:
        for cls in classes:
            f.write(cls + "\n")

    # Preparing the data.yaml
    data = {
        'train': "training_data/train/images",
        'val'  : "training_data/val/images",
        'nc': len(classes),
        'names': {i: name for i, name in enumerate(classes)}
    }

    # Store the final outputs 
    # This file is useful for the model training
    with open("data.yaml", "w") as f:
        yaml.dump(data, f, sort_keys=False)
