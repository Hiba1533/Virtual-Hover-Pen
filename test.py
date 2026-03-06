import cv2
import mediapipe as mp
import numpy as np
import time
import os

#initialization
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

#open webcam
cap = cv2.VideoCapture(0)

#drawing variables
canvas = None
prev_x, prev_y = 0, 0

brush_color = (255, 0, 0)
eraser_mode = False
drawing = False
show_instructions = True

#screenshot controls
last_screenshot_time = 0
screenshot_cooldown = 2

#create folder to store ss
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# ------------------ FUNCTIONS ------------------
#screenshot 
def take_screenshot(canvas):
    filename = f"screenshots/screenshot_{int(time.time())}.png"
    cv2.imwrite(filename, canvas)
    print("Screenshot saved:", filename)

def clear_canvas():
    global canvas
    canvas[:] = 0
    print("Canvas cleared")

def is_thumb_up(lm):
    return (
        lm[4][1] < lm[3][1] and
        lm[8][1] > lm[6][1] and
        lm[12][1] > lm[10][1] and
        lm[16][1] > lm[14][1] and
        lm[20][1] > lm[18][1]
    )

def get_brush_thickness(lmList):
    x1, y1 = lmList[4]
    x2, y2 = lmList[8]
    distance = int(np.hypot(x2 - x1, y2 - y1))
    thickness = np.interp(distance, [20, 150], [2, 25])
    return int(thickness)

def draw_instructions(canvas):
    overlay = canvas.copy()
    if show_instructions:
        cv2.rectangle(overlay, (0, 0), (300, 120), (20, 20, 20), -1)
        canvas[:] = cv2.addWeighted(overlay, 0.5, canvas, 0.5, 0)
        y = 18
        step = 16
        def text(t, y):
            cv2.putText(canvas, t, (8, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1)
        text("Index finger  : Free draw", y); y+=step
        text("Thumb up      : Save", y); y+=step
        text("R G B Y       : Colors", y); y+=step
        text("E             : Erase", y); y+=step
        text("C             : Clear", y); y+=step
        text("H             : Toggle Info", y)

# ------------------ MAIN LOOP ------------------
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

#creating black canvas
    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = [(int(lm.x*w), int(lm.y*h)) for lm in handLms.landmark]
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            x1, y1 = lmList[8]  # Index tip

            # Screenshot
            if is_thumb_up(lmList):
                if time.time() - last_screenshot_time > screenshot_cooldown:
                    take_screenshot(canvas)
                    last_screenshot_time = time.time()

#index finger
            index_up = lmList[8][1] < lmList[6][1]

            # ---- FREEHAND DRAWING ----
            if index_up:
                drawing = True
                color = (0,0,0) if eraser_mode else brush_color
                thickness = 40 if eraser_mode else get_brush_thickness(lmList)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x1, y1

                sx = int(prev_x*0.7 + x1*0.3)
                sy = int(prev_y*0.7 + y1*0.3)

                cv2.line(canvas, (prev_x, prev_y), (sx, sy), color, thickness)
                prev_x, prev_y = sx, sy

            else:
                drawing = False
                prev_x, prev_y = 0, 0

    draw_instructions(canvas)

    # Brush thickness preview
    if not eraser_mode:
        cv2.circle(canvas, (50, h-50), brush_thickness if 'brush_thickness' in locals() else 5, brush_color, -1)

    cv2.imshow("Webcam", img)
    cv2.imshow("Canvas", canvas)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('r'):
        brush_color = (0,0,255); eraser_mode=False
    elif key == ord('g'):
        brush_color = (0,255,0); eraser_mode=False
    elif key == ord('b'):
        brush_color = (255,0,0); eraser_mode=False
    elif key == ord('y'):
        brush_color = (0,255,255); eraser_mode=False
    elif key == ord('e'):
        eraser_mode = True
    elif key == ord('c'):
        clear_canvas()
    elif key == ord('p'):
        take_screenshot(canvas)
    elif key == ord('h'):
        show_instructions = not show_instructions

#program termination
cap.release()
cv2.destroyAllWindows()
