# 🧠 Object Identification use case using YOLO 

This project offers a robust end-to-end pipeline for object detection in PDF documents using YOLO. It integrates **custom PDF-to-image conversion**, **interactive annotation tools**, **dynamic training strategies**, and **multi-stage inference capabilities** using both **custom-trained** and **pre-trained YOLO models**.

---

## 🔍 Key Capabilities

* 📤 **Smart PDF Handling**
  Seamlessly uploads and auto-converts multiple PDFs to annotated image datasets.

* 🎨 **GUI-based Annotation Tool**
  Built using OpenCV, enabling real-time bounding box drawing, label assignment, and dynamic label management.

* 🔀 **Modular Workflow**
  Clean separation between PDF preprocessing, annotation, training, and inference stages — allowing flexible usage and easy debugging.

* 🧠 **YOLO-Based Training Architecture**
  Supports both **single-shot training** and **multi-approach experimentation** for optimal model performance.

* 🧪 **Looped Validation**
  Ensures a valid testing file is supplied by incorporating an interactive loop that re-prompts on error or absence.

* 📊 **Page-by-Page Inference and Output**
  Results are organized on a per-page basis, annotated with bounding boxes and labels, and stored for analysis or report generation.

---

## 🚀 Project Workflow

### 🔸 Option 1: Train a Custom Object Detection Model

#### 1. 📁 PDF Input & Dataset Structuring

* User uploads one or more PDF documents in pdf's folder. 
* Automatically splits pages into:

  * `train/`
  * `val/`
  * (optional) `test/`
* Internally handled via `pdf2image.py` and supports batch PDF input.

#### 2. 🖊 Annotation with GUI

* Run with:

  ```bash
  python annotation.py
  ```
* Features:

  * Mouse-based bounding box creation
  * Real-time label entry and management
  * Saves annotations in YOLO format (`.txt`)
  * Creates dataset YAML and class definition files automatically

#### 3. 🧠 Multi-Approach Model Training

* After annotation, user is prompted:

  ```
  How many training approaches do you want to run?
  ```
* Saves best model as:

  ```
  trained_model/custom_model/weights/best.pt
  ```

#### 4. 🧪 Inference and Testing

* User places a testing PDF into `testing_data/`.
* The system initiates a **while loop** to ensure a valid file is present.
* Each page is converted to an image → passed to the model → annotated results are saved in:

  ```
  results/page_1.jpg, page_2.jpg, ...
  ```

---

### 🔸 Option 2: Use a Pre-Trained Model customized by me

1. Ensure `pretrained_model.pt` is available.
2. Place your test PDF in the `testing_data/` directory.
3. The system:

   * Converts the PDF to images
   * Applies the pre-trained model in `Object Detection.py` itself
   * Outputs results into the `results/` directory

---

## 🧱 Project Structure

```
project/
├── annotation.py            # GUI-based annotation tool (Option 1)
├── model.py                 # Model training (Option 1)
├── pdf2image.py             # PDF-to-image conversion module (Option 1) & (Option 2)
├── object_detection.py      # Core detection pipeline (YOLO inference)
├── pretrained_model.pt      # Pre-trained model weights (used in Option 2)
├── requirements.txt         # Python dependencies
├── pdf1.pdf                 # Input PDF files need to be uploaded in the pdf's folder
├── pdf2.pdf
├── pdf3.pdf
├── pdf4.pdf
├── pdf5.pdf
├── test.pdf                 # After training the model or before using the pre-trained model, you need place the test.pdf in the testing_data (folder will be created automatically)

```
---

## ⚙️ Configuration & Requirements

* **Python:** >= 3.8
* **Dependencies:**

  ```text
  opencv-python
  pymupdf
  pyyaml
  ultralytics
  ```
* **Installation:**

  ```bash
  pip install -r requirements.txt
  ```

---

## 📦 Modes of Operation

| Mode        | Tools Required                              | PDF Handling                                       | Manual Setup                                                          |
| ----------- | ------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| Train Model | `annotation.py`, `model.py`, `pdf2image.py`,`Object Detection.py` | Manual: User must place the pdf's in the `pdf's folder` | Yes: must also manually place a testing PDF in `testing_data/` if not provided initially |
| Pre-trained | `pretrained_model.pt`, `pdf2image.py`,`Object Detection.py`                  | No need of any training pdf's | Only testing PDF must be placed in `testing_data/` folder manually    |

---

## ✅ Future Extensions (Suggestions)

* Add **FastAPI interface** for web-based usage
* Enable **multi-label**
* Add support for other file formats (e.g., Word, Excel)
* Enhance auto-labeling with weak supervision or active learning

---

## 🚀 How to Run

1. Clone the repository  
2. Install dependencies
3. Place your pdf's in a proper way
4. Run the script

```bash
git clone https://github.com/paavansirivardhan123/Object_Identification_use_case_using_YOLO.git
cd Object_Identification_use_case_using_YOLO
pip install -r requirements.txt
python Object Detection.py
```

--- 

## 👤 Author

**Name:** Paavan Siri Vardhan Narava  
**Location:** India  
**Contact:** Contributions and collaborations are welcome! Feel free to reach out or credit the work.
