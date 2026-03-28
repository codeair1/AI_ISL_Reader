import os
import cv2

DATA_DIR = './data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
dataset_size = 100

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not detected")
    exit()

for letter in letters:

    class_index = letters.index(letter)
    class_path = os.path.join(DATA_DIR, str(class_index))

    if not os.path.exists(class_path):
        os.makedirs(class_path)

    print(f'Collecting data for letter {letter} (class {class_index})')

    # Wait for user to start
    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        cv2.putText(frame, f'Letter {letter} (Class {class_index}) - Press Q to start',
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # 1 second pause
    ret, frame = cap.read()
    cv2.putText(frame, 'Get Ready...',
                (150, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 255),
                3)
    cv2.imshow('frame', frame)
    cv2.waitKey(1000)

    # 3 second countdown
    for i in range(3, 0, -1):
        ret, frame = cap.read()
        cv2.putText(frame, f'Starting in {i}',
                    (150, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (0, 255, 0),
                    3)
        cv2.imshow('frame', frame)
        cv2.waitKey(1000)

    # Capture images
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()

        if not ret:
            continue

        cv2.putText(frame, f'Capturing {letter}: {counter}/{dataset_size}',
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2)

        cv2.imshow('frame', frame)

        cv2.imwrite(os.path.join(class_path, f'{counter}.jpg'), frame)

        counter += 1
        cv2.waitKey(30)

    print(f'Finished collecting letter {letter}')

    # Wait before next class
    while True:
        ret, frame = cap.read()

        cv2.putText(frame, 'Press N for next letter',
                    (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 0),
                    2)

        cv2.imshow('frame', frame)

        key = cv2.waitKey(25) & 0xFF
        if key == ord('n'):
            break

cap.release()
cv2.destroyAllWindows()