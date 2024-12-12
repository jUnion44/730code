import cv2
import mediapipe as mp
from picamera2 import Picamera2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.6,
                       min_tracking_confidence=0.6)
mp_drawing = mp.solutions.drawing_utils

def is_finger_up(landmarks, finger_tip, finger_pip, finger_mcp):
    return (landmarks[finger_tip].y < landmarks[finger_pip].y < landmarks[finger_mcp].y)
def is_thumb_up(landmarks, finger_tip, finger_pip, finger_mcp, handedness):
    if handedness == "right": # mediapipe has handedness backwards somehow
        return (landmarks[finger_tip].x < landmarks[finger_pip].x < landmarks[finger_mcp].x)
    else:
        return (landmarks[finger_tip].x > landmarks[finger_pip].x > landmarks[finger_mcp].x)

def process_frame(frame):
   result = hands.process(frame)
   if result.multi_hand_landmarks:
        print("hand found")
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)        
            landmarks = hand_landmarks.landmark

            finger_up1 = is_thumb_up(
                landmarks,
                finger_tip=mp_hands.HandLandmark.THUMB_TIP,
                finger_pip=mp_hands.HandLandmark.THUMB_IP,
                finger_mcp=mp_hands.HandLandmark.THUMB_MCP,
                handedness=result.multi_handedness[0].classification[0].label
            )
            
            finger_up2 = is_finger_up(
                landmarks,
                finger_tip=mp_hands.HandLandmark.INDEX_FINGER_TIP,
                finger_pip=mp_hands.HandLandmark.INDEX_FINGER_PIP,
                finger_mcp=mp_hands.HandLandmark.INDEX_FINGER_MCP
            )

            finger_up3 = is_finger_up(
                landmarks,
                finger_tip=mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                finger_pip=mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                finger_mcp=mp_hands.HandLandmark.MIDDLE_FINGER_MCP
            )

            finger_up4 = is_finger_up(
                landmarks,
                finger_tip=mp_hands.HandLandmark.RING_FINGER_TIP,
                finger_pip=mp_hands.HandLandmark.RING_FINGER_PIP,
                finger_mcp=mp_hands.HandLandmark.RING_FINGER_MCP
            )

            finger_up5 = is_finger_up(
                landmarks,
                finger_tip=mp_hands.HandLandmark.PINKY_TIP,
                finger_pip=mp_hands.HandLandmark.PINKY_PIP,
                finger_mcp=mp_hands.HandLandmark.PINKY_MCP
            )

        return not finger_up1 and finger_up2 and not finger_up3 and not finger_up4 and not finger_up5

if __name__ == "__main__":
    print("CAMERA IN USE")
    # Start capturing from the camera
    camera = Picamera2()
    print("CAMERA ON")
    camera_config = camera.create_preview_configuration()
    camera.configure(camera_config)
    camera.start()

    while True:
        frame = camera.capture_array()[:, :, :3]
        # if not ret:
        #     break

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        result = hands.process(frame)
        # print(dir(mp_hands.HandLandmark))

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
            
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
                landmarks = hand_landmarks.landmark

                
                finger_up = is_finger_up(
                    landmarks,
                    finger_tip=mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    finger_pip=mp_hands.HandLandmark.INDEX_FINGER_PIP,
                    finger_mcp=mp_hands.HandLandmark.INDEX_FINGER_MCP
                )

                finger_up2 = is_finger_up(
                    landmarks,
                    finger_tip=mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    finger_pip=mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                    finger_mcp=mp_hands.HandLandmark.MIDDLE_FINGER_MCP
                )

                finger_up3 = is_finger_up(
                    landmarks,
                    finger_tip=mp_hands.HandLandmark.RING_FINGER_TIP,
                    finger_pip=mp_hands.HandLandmark.RING_FINGER_PIP,
                    finger_mcp=mp_hands.HandLandmark.RING_FINGER_MCP
                )

                finger_up4 = is_finger_up(
                    landmarks,
                    finger_tip=mp_hands.HandLandmark.PINKY_TIP,
                    finger_pip=mp_hands.HandLandmark.PINKY_PIP,
                    finger_mcp=mp_hands.HandLandmark.PINKY_MCP
                )

                finger_up5 = is_thumb_up(
                    landmarks,
                    finger_tip=mp_hands.HandLandmark.THUMB_TIP,
                    finger_pip=mp_hands.HandLandmark.THUMB_IP,
                    finger_mcp=mp_hands.HandLandmark.THUMB_MCP
                )

                if finger_up:
                    cv2.putText(frame, "INDEX", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if finger_up2:
                    cv2.putText(frame, "MIDDLE", (50, 80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if finger_up3:
                    cv2.putText(frame, "RING", (50, 110), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if finger_up4:
                    cv2.putText(frame, "PINKY", (50, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if finger_up5:
                    cv2.putText(frame, "THUMB", (50, 170), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # cv2.imshow('Tracker', frame)
        cv2.imwrite("test.png", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cap.release()
    # cv2.destroyAllWindows()