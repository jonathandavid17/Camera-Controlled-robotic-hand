# Camera-controlled-robotic-hand
A low-cost, camera-controlled robotic hand built with cardboard, Arduino, and computer vision.

Built solo for the Featherless.ai hackathon (GIBC V2).

[Watch demo video + Explanation](https://youtu.be/nmQNqolrdHY)

## How it works
1. Python reads frames from the webcam and mirrors them.
2. cvzone's HandDetector uses MediaPipe hand tracking to detect a hand and determine the open/closed state of each finger.
3. The script converts each finger's open/closed state to a servo angle (0 or 180 degrees) and sends all five as one line over serial.
4. The Arduino reads the line, checks that it got all five values, and writes each angle to its servo.
5. Each servo pulls a fishing-line tendon that runs through straw guides to a fingertip, so the cardboard finger curls.

## Serial protocol
One line per update at 9600 baud:

`index,middle,thumb,ring,pinky\n`

Each value is an integer from 0 to 180 (for example `180,0,180,180,0`). The Arduino ignores any line that doesn't contain exactly five values.

The index and pinky values are inverted in software (`1 - f`) because those servos are mounted facing the opposite direction inside the hand's base.

## Hardware
1. Arduino Uno: Connected to the laptop over USB
2. 5x SG90 micro servos: One per finger
3. Cardboard hand: Mechanical frame
4. Plastic drinking straws: guide channels for the tendons
5. Fishing line: Tendons from fingertips to servo horns
6. Breadboard and jumper wires	
7. 4x AA battery holder: Powers the servos 
8. Laptop with a webcam	

## Servo wiring
Fingers and their respective pins 

Index = 2

Middle = 3

Thumb = 4

Ring = 5

Pinky = 6

cvzone reports the fingers as [thumb, index, middle, ring, pinky]; the script reorders them to [index, middle, thumb, ring, pinky] to match the Arduino servo assignments.

Connect each servo's signal wire to its corresponding Arduino pin. 
Connect the servo power supply's ground to Arduino GND so they share a common ground.

[view the circuit in tinkercad](https://www.tinkercad.com/things/eKE3Kj0RcgY-funky-waasa)


## Prerequisites
A) Software
- Python 3.13.7

- Arduino IDE (the `Servo` library is included)

- Python packages, pinned in `requirements.txt`: cvzone 2.0.0, MediaPipe 1.0.1, OpenCV (opencv-python and opencv-contrib-python 5.0.0.93), pySerial 3.5

- Tested on Windows 11 with the Arduino on `COM5`

B) Hardware
- Laptop with a webcam

- Arduino Uno and USB cable

- 5x SG90 micro servos

- The cardboard hand (cardboard frame, plastic straws, fishing line)

- Breadboard and jumper wires

- 4x AA battery holder for servo power

You can run the vision side with only a webcam. The script still tracks your hand and prints the values it would send, even with no Arduino connected.


## Setup

1. Clone the repo
```
   git clone https://github.com/jonathandavid17/Camera-controlled-robotic-hand
```
2. Install the Python packages (a virtual environment is recommended)
```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
```
3. Upload the Arduino sketch: Open `CAMERA_ROBOTHAND/CAMERA_ROBOTHAND.ino` in the Arduino IDE, choose Arduino Uno and your port, and upload.
4. Wire the servos to pins 2 (index), 3 (middle), 4 (thumb), 5 (ring), and 6 (pinky). Power the servos from a 4x AA battery pack, and connect the battery's negative wire and an Arduino GND pin to the same ground rail.
5. Set your serial port: In `hand_tracking_5fingers.py`, change `PORT = 'COM5'` to your port if it's different (see Tools > Port in the Arduino IDE).
6. Close the Arduino Serial Monitor. If it is open, Python can't connect to the port.

## Usage
`python hand_tracking_5fingers.py`

Run it from the repo folder. The hand tracking model file `hand_landmarker.task` (about 8 MB, Google's MediaPipe Hand Landmarker model) is included in the repository and is required for hand tracking.
- Hold one hand in front of the webcam. The hand skeleton is drawn on screen, and the mechanical hand reproduces your fingers' open/closed states.
 
- The terminal prints each payload as it is sent.

- Press `q` in the video window to quit. This also closes the serial port so it's free for your next run.

## Troubleshooting
Problems and solutions

1. Could not open COM5: Port unavailable. The board may be unplugged, the selected COM port may be incorrect, or the Serial Monitor may already be using the port.

2. First commands are ignored: The Arduino resets when the serial connection opens. The script waits 2 seconds for this, so don't remove that delay.

3. A finger moves in reverse: The servo is mounted in the opposite orientation. Apply or remove the `(1 - f)` inversion for that finger in the payload mapping.

## Total Cost
| Component | Cost |
|---|---:|
| Arduino Uno | $3.41 |
| 5× SG90 servo motors | $4.45 |
| Jumper wires | $0.56 |
| 4× AA battery holder | $0.20 |
| Cardboard, straws, fishing line | $0.00 |
| **Total** | **$8.62** |

Excluding the laptop, webcam, and other equipment already available to me.



## AI assistance disclosure
1. Gemini helped with the hand detector and camera setup in `hand_tracking_5fingers.py` and helped clean up the code. It did not write the finger-to-servo mapping. The lines that read `detector.fingersUp`, reorder the fingers to match the Arduino order, invert the index and pinky, scale to 0/180 degrees, and build the payload string are my own.
2. ChatGPT helped improve the Arduino code (`CAMERA_ROBOTHAND.ino`) so the servos only move once all five values have been received in loop().
3. Claude (Anthropic) assisted with drafting most of this README. I reviewed and edited the content, formatting, and wording.
4. Gemini helped write most of the script for the presentation video while the ideas came from me.

Credits: 

Hand tracking: cvzone and MediaPipe, with OpenCV.

Hand tracking model: `hand_landmarker.task`, the MediaPipe Hand Landmarker model from Google.

Serial communication: pySerial.

Arduino `Servo` library: `#include <Servo.h>`

