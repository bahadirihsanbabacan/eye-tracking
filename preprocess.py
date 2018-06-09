import cv2
import settings
from tqdm import tqdm


def compute_area(eyes):
    a = []
    for _, (a1, _, _), (a2, _, _) in eyes:
        a.append(a1)
        a.append(a2)
    return sum(a) / len(a)


def get_eyes(image_filenames):
    face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('assets/haarcascade_eye.xml')

    for filename in tqdm(image_filenames):
        img_orig = cv2.imread(filename)
        img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(img_gray)

        assert len(faces) > 0

        x_face, y_face, w_face, h_face = faces[0]

        img_face = img_gray[y_face:y_face + h_face, x_face:x_face + w_face]

        eyes = eye_cascade.detectMultiScale(img_face)

        assert len(eyes) >= 2

        x1, y1, w1, h1 = eyes[0]
        eye1 = img_face[y1:y1 + h1, x1:x1 + w1]
        eye1 = cv2.resize(eye1, (settings.IMAGE_SIZE, settings.IMAGE_SIZE))

        x1, y1, w1, h1 = eyes[1]
        eye2 = img_face[y1:y1 + h1, x1:x1 + w1]
        eye2 = cv2.resize(eye2, (settings.IMAGE_SIZE, settings.IMAGE_SIZE))

        yield img_face, eye1, eye2
