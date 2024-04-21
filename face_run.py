import cv2
import logging, os
# logging.disable(logging.WARNING)
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from keras.models import model_from_json
import numpy as np


def run_emotion_detection(video_path):
    json_file = open("emotionfacedetect2.json", "r")
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights("emotionfacedetect2.h5")

    haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(haar_file)

    def extract_features(image):
        feature = np.array(image)
        feature = feature.reshape(1, 48, 48, 1)
        return feature / 255.0

    labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

    video = cv2.VideoCapture(video_path)
    results = {label: {'count': 0, 'total_confidence': 0} for label in labels.values()}

    while True:
        ret, im = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(im, 1.3, 5)

        try:
            for (p, q, r, s) in faces:
                image = gray[q:q + s, p:p + r]
                cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
                image = cv2.resize(image, (48, 48))
                img = extract_features(image)
                pred = model.predict(img, verbose=0)
                prediction_label = labels[pred.argmax()]
                confidence = pred.max()
                results[prediction_label]['count'] += 1
                results[prediction_label]['total_confidence'] += confidence
                # cv2.putText(im, '%s: %.2f' % (prediction_label, confidence), (p - 10, q - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
                
        except cv2.error:
            pass

    video.release()
    cv2.destroyAllWindows()

    max_count = max(data['count'] for data in results.values())
    for emotion, data in results.items():
        count = data['count']
        total_confidence = data['total_confidence']
        if count != 0:
            normalized_confidence = total_confidence / max_count
            results[emotion]['total_confidence'] = normalized_confidence
        else:
            results[emotion]['total_confidence'] = 0

    sorted_results = {k: v['total_confidence'] for k, v in sorted(results.items(), key=lambda item: item[1]['total_confidence'], reverse=True)}
    return sorted_results


if __name__ == '__main__':
    video_path = "videos/recording1.mp4"
    emotion_results = run_emotion_detection(video_path)
    print(emotion_results)