import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
cap.set(3, 720) 
cap.set(4, 420) 

# Initialize keyboard controller
keyboard = Controller()

# Finger tip indices for gesture detection
ungliya = [4, 8, 12, 16, 20]  

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Camera nhi khul rha h!!!")
        continue

    # Flip the image horizontally for mirror effect and convert to RGB
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image for hand detection
    image_rgb.flags.writeable = False
    results = hands.process(image_rgb)
    image_rgb.flags.writeable = True
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Check for hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = 0
            for tip_id in ungliya[1:]:  
                tip_y = hand_landmarks.landmark[tip_id].y
                base_y = hand_landmarks.landmark[tip_id - 2].y 
                if tip_y < base_y:  
                    fingers_up += 1

            if fingers_up >= 3: 
                keyboard.press(Key.right)  
                keyboard.release(Key.left)
                cv2.putText(image, "Accelerate (Right)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else: 
                keyboard.press(Key.left) 
                keyboard.release(Key.right)
                cv2.putText(image, "Brake (Left)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        cv2.putText(image, "No Hand Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Gesture-Controlled Hill Climb Racing", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()