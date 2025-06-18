import cv2
import mediapipe as mp
import pyautogui
 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

camera = cv2.VideoCapture(1)

def jari_terbuka(landmarks, hand_label):
    """
    Fungsi untuk menghitung jari yang terbuka.
    """
    ibuJariTerbuka = False
    if hand_label == 'Right':
        if landmarks[4].x < landmarks[3].x:
            ibuJariTerbuka = True
    elif hand_label == 'Left':
        if landmarks[3].x < landmarks[4].x:
            ibuJariTerbuka = False

    # telunjuk terbuka
    telunjuk_terbuka = landmarks[8].y < landmarks[6].y

    # jari tengah
    tengah_terbuka = landmarks[12].y < landmarks[10].y

    # jari manis
    manis_terbuka = landmarks[16].y < landmarks[14].y
    
    # kelingking
    kelingking_terbuka = landmarks[20].y < landmarks[18].y      
    

    # jumlah jari terbuka
    jariTerbukaSum = sum([ibuJariTerbuka, telunjuk_terbuka, tengah_terbuka, manis_terbuka, kelingking_terbuka])

    return jariTerbukaSum, ibuJariTerbuka, telunjuk_terbuka, tengah_terbuka, manis_terbuka, kelingking_terbuka


with mp_hands.Hands(
    model_complexity = 0,
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
) as hands:
    

    # default text
    gesture_text = "TIDAK DIKENALI"
    last_gesture = ''

    while True:
        sts, frame = camera.read()

        if not sts:
            break

        # timpa aja wkwkkw, ngeflip horizontally
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                hand_label = result.multi_handedness[hand_idx].classification[0].label

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # dapatkan info jari terbuka
                jumlah_terbuka, ibuJari, jariTelunjuk, jariTengah, jariManis, jariKelingking = jari_terbuka(hand_landmarks.landmark, hand_label)


                if jumlah_terbuka == 5:
                    gesture_text = 'JUMP'
                elif jumlah_terbuka == 1 and jariTelunjuk:
                    gesture_text = 'LEFT'
                elif jumlah_terbuka == 2 and jariTelunjuk and jariTengah:
                    gesture_text = 'RIGHT'
                elif jumlah_terbuka == 0:
                    gesture_text = 'ROLL'

        if gesture_text != last_gesture:
            if gesture_text == 'JUMP':
                pyautogui.press('up')
            elif gesture_text == 'LEFT':
                pyautogui.press('left')
            elif gesture_text == 'RIGHT':
                pyautogui.press('right')
            elif gesture_text == 'ROLL':
                pyautogui.press('down')

        last_gesture = gesture_text


        cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow('Gesture Control Subway Sufers', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    
camera.release()
cv2.destroyAllWindows()