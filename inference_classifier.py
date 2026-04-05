import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)

labels_dict = {i: chr(65 + i) for i in range(26)}  # 0->A, 1->B ...

while True:
    data_aux = []

    ret, frame = cap.read()
    if not ret:
        continue

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:

        detected_hands = results.multi_hand_landmarks[:2]

        for hand_landmarks in detected_hands:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x)
                data_aux.append(lm.y)

    # Ensure fixed size = 84 features
    while len(data_aux) < 84:
        data_aux.append(0)

    if len(data_aux) == 84:
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        cv2.putText(frame, predicted_character,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 255, 0),
                    4)

    cv2.imshow('Sign Language Detector', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()