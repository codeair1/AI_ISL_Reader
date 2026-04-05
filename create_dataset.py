import os
import pickle
import mediapipe as mp
import cv2

DATA_DIR = './data'

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

data = []
labels = []

for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):

        data_aux = []

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:

            detected_hands = results.multi_hand_landmarks[:2]

            for hand_landmarks in detected_hands:
                print(f"{hand_landmarks}- ")
                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x)
                    data_aux.append(lm.y)
                    print(f"[{lm.x},{lm.y}]")

        # ensure fixed length (84)
        while len(data_aux) < 84:
            data_aux.append(0)

        if len(data_aux) == 84:
            data.append(data_aux)
            labels.append(dir_)

with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Dataset created successfully")
print("Samples:", len(data))