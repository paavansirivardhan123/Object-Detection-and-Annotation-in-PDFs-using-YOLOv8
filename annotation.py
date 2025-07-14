import cv2
from pathlib import Path
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


def process_images(image_dir, label_dir, classes):
    import os 
    os.makedirs(label_dir, exist_ok=True)
    image_paths = list(Path(image_dir).glob("*.jpg"))

    for image_path in image_paths:
        annotations, img = annotate_image(str(image_path))  
        h, w = img.shape[:2] 
        boxes = []

        for ann in annotations:
            label = ann["label"]
            box = ann["box"]
            if label not in classes:
                classes.append(label)
            class_index = classes.index(label)

            x1, y1, x2, y2 = box
            x_center = (x1 + x2) / 2 / w
            y_center = (y1 + y2) / 2 / h
            width = abs(x2 - x1) / w
            height = abs(y2 - y1) / h
            boxes.append((class_index, x_center, y_center, width, height))

        label_save_path = os.path.join(label_dir, f"{image_path.stem}.txt")

        with open(label_save_path, "w") as f:
            for box in boxes:
                class_id, x_center, y_center, width, height = box

                if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and width > 0 and height > 0):
                    continue
                
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


def main():
    import yaml
    classes = []

    process_images("training_data/train/images", "training_data/train/labels", classes)
    process_images("training_data/val/images", "training_data/val/labels", classes)

    with open("classes.txt", "w") as f:
        for cls in classes:
            f.write(cls + "\n")

    data = {
        'train': "training_data/train/images",
        'val'  : "training_data/val/images",
        'nc': len(classes),
        'names': {i: name for i, name in enumerate(classes)}
    }

    with open("data.yaml", "w") as f:
        yaml.dump(data, f, sort_keys=False)
