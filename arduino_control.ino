#include <Servo.h>
#include <ArduinoSTL.h> // Go to ArduinoSTL>src>new_handler and comment out line 22 (const std::nothrow_t std::nothrow = { };)
#include <vector>
 
// pin numbers and constants
#define SERVO0 11  //Thumb
#define SERVO1 10  //Index
#define SERVO2 9   //Middle
#define SERVO3 6   //Ring
#define SERVO4 5   //Pinky

const int ANGLE_DIVISIONS = 1;
const int TIME_DELAY = 15;

// creating servo objects
Servo thumb_servo;
Servo index_servo;
Servo middle_servo;
Servo ring_servo;
Servo pinky_servo;

std::vector<Servo> SERVO_LIST{ thumb_servo, index_servo, middle_servo, ring_servo, pinky_servo };

void setup() {
  Serial.begin(9600);
  thumb_servo.attach(SERVO0);
  index_servo.attach(SERVO1);
  middle_servo.attach(SERVO2);
  ring_servo.attach(SERVO3);
  pinky_servo.attach(SERVO4);
  pinMode(13,OUTPUT);
  // initializing all servos to 0 position
  for (int i = 0; i < SERVO_LIST.size(); i++) {
    SERVO_LIST[i].write(0);
  }
  delay(2000);
}

void move_servo(Servo& servo_num, int end_angle) {
  int current_angle = servo_num.read();
  if (current_angle < end_angle) {
    for (int pos = current_angle; pos <= end_angle; pos += ANGLE_DIVISIONS) {
      servo_num.write(pos);
      delay(TIME_DELAY);
    }
  } else {
    for (int pos = current_angle; pos >= end_angle; pos -= ANGLE_DIVISIONS) {
      servo_num.write(pos);
      delay(TIME_DELAY);
    }
  }
}

void holdUpFinger(int holdup_servonum) {
  for (int servonum = 0; servonum < SERVO_LIST.size(); servonum++) {
    if (servonum != holdup_servonum) {
      move_servo(SERVO_LIST[servonum], 0);
    } else {
      // Set the servo angle to 0 degrees
      move_servo(SERVO_LIST[servonum], 180);
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    int state = Serial.parseInt();
    if (state == 2){
      digitalWrite(13,HIGH);
    }
   
    switch (state) {
      case 1:
        // all fingers unclenched
        for (int i = 0; i < SERVO_LIST.size(); i++) {
          SERVO_LIST[i].write(0);
        }
        break;

      case 2:
        // clench thumb
        holdUpFinger(0);
        break;

      case 3:
        // clench index
        holdUpFinger(1);
        break;

      case 4:
        // clench middle
        holdUpFinger(2);
        break;

      case 5:
        // clench ring
        holdUpFinger(3);
        break;

      case 6:
        // clench pinky
        holdUpFinger(4);
        break;

      case 7:
        // clench all
        for (int i = 0; i < SERVO_LIST.size(); i++) {
          SERVO_LIST[i].write(180);
        }
        break;
    }
    exit(0);
  }
}
