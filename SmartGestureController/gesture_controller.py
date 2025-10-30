import cv2
import mediapipe as mp
import pyautogui
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

gesture_text = ""
x_buffer, y_buffer = [], []
zoom_prev_distance = None
last_gesture_time = 0
gesture_cooldown = 0.5  # Faster response time

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    hand_positions = []

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            # Optional: comment out to improve speed
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            wrist_x = int(handLms.landmark[mp_hands.HandLandmark.WRIST].x * w)
            wrist_y = int(handLms.landmark[mp_hands.HandLandmark.WRIST].y * h)
            hand_positions.append((wrist_x, wrist_y))

        # Zoom logic
        if len(hand_positions) == 2:
            dist = math.hypot(hand_positions[1][0] - hand_positions[0][0],
                              hand_positions[1][1] - hand_positions[0][1])
            current_time = time.time()
            if zoom_prev_distance is not None:
                delta = dist - zoom_prev_distance
                if delta > 40 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.hotkey('ctrl', '+')
                    gesture_text = "🔍 Zoom In"
                    last_gesture_time = current_time
                elif delta < -40 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.hotkey('ctrl', '-')
                    gesture_text = "🔎 Zoom Out"
                    last_gesture_time = current_time
            zoom_prev_distance = dist
        else:
            zoom_prev_distance = None

        # Swipe/Scroll logic
        handLms = result.multi_hand_landmarks[0]
        wrist_x = handLms.landmark[mp_hands.HandLandmark.WRIST].x * w
        wrist_y = handLms.landmark[mp_hands.HandLandmark.WRIST].y * h
        x_buffer.append(wrist_x)
        y_buffer.append(wrist_y)

        if len(x_buffer) > 5:
            x_buffer.pop(0)
        if len(y_buffer) > 5:
            y_buffer.pop(0)

        if len(x_buffer) == 5 and len(y_buffer) == 5:
            delta_x = x_buffer[-1] - x_buffer[0]
            delta_y = y_buffer[-1] - y_buffer[0]
            current_time = time.time()

            if abs(delta_x) > abs(delta_y):
                if delta_x > 50 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.press('right')
                    gesture_text = "→ Next Slide"
                    last_gesture_time = current_time
                    x_buffer.clear()
                    y_buffer.clear()
                elif delta_x < -50 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.press('left')
                    gesture_text = "← Previous Slide"
                    last_gesture_time = current_time
                    x_buffer.clear()
                    y_buffer.clear()
            else:
                if delta_y < -50 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.press('up')
                    gesture_text = "↑ Scroll Up"
                    last_gesture_time = current_time
                    x_buffer.clear()
                    y_buffer.clear()
                elif delta_y > 50 and current_time - last_gesture_time > gesture_cooldown:
                    pyautogui.press('down')
                    gesture_text = "↓ Scroll Down"
                    last_gesture_time = current_time
                    x_buffer.clear()
                    y_buffer.clear()
    else:
        x_buffer.clear()
        y_buffer.clear()
        zoom_prev_distance = None
        gesture_text = ""

    if gesture_text:
        cv2.putText(frame, gesture_text, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    cv2.imshow("🖐️ Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
