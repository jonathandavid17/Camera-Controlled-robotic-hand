import cv2
import serial
import time
from cvzone.HandTrackingModule import HandDetector

# --- Arduino Serial Setup ---
PORT = 'COM5'
BAUD_RATE = 9600

try:
    arduino = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    # CRITICAL: Wait 2 seconds for Arduino auto-reset on connection
    time.sleep(2)
    print(f"Connected successfully to Arduino on {PORT}")
except Exception as e:
    print(f"Could not open {PORT}: {e}")
    print("Check if Arduino IDE Serial Monitor is open or if you're on the right COM port.")
    arduino = None

# --- Hand Detector & Camera Setup ---
detector = HandDetector(maxHands=1, detectionCon=0.7)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Find hands and draw bounding box / skeleton
    hands, frame = detector.findHands(cv2.flip(frame, 1))

    if hands:
        # Array of 5 binary finger states: [Thumb, Index, Middle, Ring, Pinky]
        f = detector.fingersUp(hands[0])

        # Map 1/0 states to 180° / 0° matching your Arduino order:
        # Index (f[1]), Middle (f[2]), Thumb (f[0]), Ring (f[3]), Pinky (f[4])
        payload = payload = f"{(1-f[1])*180},{(f[2])*180},{(f[0])*180},{(f[3])*180},{(1-f[4])*180}\n"
        print(payload.strip())

        if arduino and arduino.is_open:
            arduino.write(payload.encode())

    cv2.imshow("Hand Tracking Servo Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
if arduino and arduino.is_open:
    arduino.close()
    print("Serial connection closed.")
