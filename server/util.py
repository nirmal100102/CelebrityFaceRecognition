import joblib
import json
import numpy as np
import base64
import cv2
import os
from wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}
__class_display_name = {
    "akshay": "Akshay Kumar",
    "kohli": "Virat Kohli",
    "messi": "Lionel Messi",
    "nora": "Nora Fatehi",
    "urvashi": "Urvashi Rautela"
}

__model = None

def classify_image(image_base64_data, file_path=None):
    print(">>> classify_image called")

    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    print(f">>> Number of cropped faces: {len(imgs)}")

    result = []
    if len(imgs) == 0:
        return []

    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((
            scalled_raw_img.reshape(32 * 32 * 3, 1),
            scalled_img_har.reshape(32 * 32, 1)
        ))

        len_image_array = 32*32*3 + 32*32
        final = combined_img.reshape(1, len_image_array).astype(float)
        prediction = __model.predict(final)[0]
        probabilities = np.around(__model.predict_proba(final) * 100, 2).tolist()[0]

        predicted_class = class_number_to_name(prediction).lower()

        result.append({
            'class': predicted_class,
            'class_probability': probabilities,
            'class_dictionary': {k.lower(): v for k, v in __class_name_to_number.items()}
        })

    print(">>> Classification result:", result)
    return result

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("./artifacts/class_dictionary.json", "r") as f:
        raw_class_dict = json.load(f)

    # Keep only the folder names as keys
    __class_name_to_number = {os.path.basename(k).lower(): v for k, v in raw_class_dict.items()}
    __class_number_to_name = {v: os.path.basename(k).lower() for k, v in raw_class_dict.items()}

    global __model
    if __model is None:
        with open('./artifacts/saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")

def get_cv2_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('C:\\Users\\Lenovo\\Documents\\code\\CelebrityFaceRecognition\\server\\opencv\\haarcascades\\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\\Users\\Lenovo\\Documents\\code\\CelebrityFaceRecognition\\server\\opencv\\haarcascades\\haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces

def get_b64_test_image_for_kohli():
    with open("b64.txt") as f:
        return f.read()
