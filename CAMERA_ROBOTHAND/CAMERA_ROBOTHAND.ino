#include <Servo.h>

// INDEX
int indexservopin = 2;
Servo indexservo;

// MIDDLE
int middleservopin = 3;
Servo middleservo;

// THUMB
int thumbservopin = 4;
Servo thumbservo;

// RING
int ringservopin = 5;
Servo ringservo;

// PINKY
int pinkyservopin = 6;
Servo pinkyservo;


void setup() {

  Serial.begin(9600);

  indexservo.attach(indexservopin);
  middleservo.attach(middleservopin);
  thumbservo.attach(thumbservopin);
  ringservo.attach(ringservopin);
  pinkyservo.attach(pinkyservopin);

}


void loop() {

   // Wait until a complete command is received
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');

    int indexAngle;
    int middleAngle;
    int thumbAngle;
    int ringAngle;
    int pinkyAngle;

    // Read all 5 angles from the same command
    int values = sscanf(
      data.c_str(),
      "%d,%d,%d,%d,%d",
      &indexAngle,
      &middleAngle,
      &thumbAngle,
      &ringAngle,
      &pinkyAngle
    );

    // Only move the hand if all 5 values were received
    if (values == 5) {
      indexservo.write(indexAngle);
      middleservo.write(middleAngle);
      thumbservo.write(thumbAngle);
      ringservo.write(ringAngle);
      pinkyservo.write(pinkyAngle);
    }
  }
}