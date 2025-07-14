import cv2
import os

annotations = []
drawing = False
label_input_mode = False
current_label = ""
ix, iy = -1, -1
curr_x, curr_y = -1, -1
box_coords = None

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, curr_x, curr_y, box_coords, label_input_mode, current_label

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        curr_x, curr_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            curr_x, curr_y = x, y
        
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        curr_x, curr_y = x, y
        box_coords = (ix, iy, curr_x, curr_y)
        label_input_mode = True
        current_label = ""

def annotate_image(image_path):
    global img, annotations, label_input_mode, current_label, box_coords, drawing

    annotations = []
    img = cv2.imread(image_path)
    clone = img.copy()

    cv2.namedWindow("Annotator")
    cv2.resizeWindow("Annotator", 600, 700) 
    cv2.setMouseCallback("Annotator", draw_rectangle)

    while True:
        display_img = img.copy()

        if drawing:
            cv2.rectangle(display_img, (ix, iy), (curr_x, curr_y), (0, 255, 255), 2)

        if label_input_mode:
            cv2.putText(display_img, f"Label: {current_label}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Annotator", display_img)
        cv2.resizeWindow("Annotator", 600, 700)

        key = cv2.waitKey(1) & 0xFF

        if label_input_mode:
            if key == 13 or key == 10: 
                annotations.append({
                    "label": current_label,
                    "box": list(box_coords)
                }) 
                cv2.rectangle(img, (box_coords[0], box_coords[1]), (box_coords[2], box_coords[3]), (0, 255, 0), 2)
                cv2.putText(img, current_label, (box_coords[0], box_coords[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                label_input_mode = False
                box_coords = None
                current_label = ""

            elif key == 8: 
                current_label = current_label[:-1]

            elif 32 <= key <= 126: 
                current_label += chr(key)

            continue 

        if key == ord("r"): 
            img = clone.copy()
            annotations = []

        elif key == ord("q"):  
            break

    cv2.destroyAllWindows()
    return annotations, img

def main():

    import os 
    
    classes = []

    image_folder = "training_data\\images"
    save_label_folder = "training_data\\labels\\"


    if not os.path.exists(save_label_folder):
        os.makedirs(save_label_folder)


    image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder)]

    for idx, image_path in enumerate(image_paths):

        annotations, img = annotate_image(image_path)

        boxes = []
        for ann in annotations:
            label = ann["label"]
            box = ann["box"]
            if label not in classes:
                classes.append(label)
            class_index = classes.index(label)
            boxes.append((class_index, *box))

        label_save_path = os.path.join(save_label_folder, f"label_{idx+1}.txt")

        with open(label_save_path, "w") as f:
            for box in boxes:
                f.write(" ".join(map(str, box)) + "\n")

    with open("classes.txt", "w") as f:
        for cls in classes:
            f.write(cls + "\n")
    

    import os
    import yaml

    data = {
        'train': "training_data/images",
        'nc': len(classes),
        'names': {i: name for i, name in enumerate(classes)}
    }
    
    with open("data.yaml", "w") as f:
        yaml.dump(data, f, sort_keys=False)



