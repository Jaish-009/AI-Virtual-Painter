import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Colors and settings
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]  # Blue, Green, Red, Eraser (Black)
color_index = 0
brush_thickness = 8
eraser_thickness = 50

# Setup canvas
cap = cv2.VideoCapture(0)
canvas = None

# Helper: check which fingers are up
def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    fingers = []
    for tip in finger_tips:
        fingers.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)
    return fingers

# Previous position for drawing
xp, yp = 0, 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror view
    h, w, c = img.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                # Tip of index finger
                x1, y1 = lm_list[8][1], lm_list[8][2]
                # Tip of middle finger
                x2, y2 = lm_list[12][1], lm_list[12][2]

                # Check fingers
                finger_state = fingers_up(handLms)

                # Selection Mode (two fingers up: index + middle)
                if finger_state[0] and finger_state[1]:
                    xp, yp = 0, 0
                    if y1 < 80:  # Choose color by moving to top
                        if 0 < x1 < 100:
                            color_index = 0  # Blue
                        elif 100 < x1 < 200:
                            color_index = 1  # Green
                        elif 200 < x1 < 300:
                            color_index = 2  # Red
                        elif 300 < x1 < 400:
                            color_index = 3  # Eraser

                    cv2.rectangle(img, (x1 - 25, y1 - 25), (x2 + 25, y2 + 25), colors[color_index], cv2.FILLED)

                # Drawing Mode (only index finger up)
                elif finger_state[0] and not finger_state[1]:
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    if color_index == 3:  # Eraser
                        cv2.line(canvas, (xp, yp), (x1, y1), (0, 0, 0), eraser_thickness)
                    else:
                        cv2.line(canvas, (xp, yp), (x1, y1), colors[color_index], brush_thickness)

                    xp, yp = x1, y1

    # Merge canvas with webcam
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # Draw color selection buttons
    cv2.rectangle(img, (0, 0), (100, 80), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (100, 0), (200, 80), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (200, 0), (300, 80), (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (300, 0), (400, 80), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "Eraser", (310, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("AI Virtual Painter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
