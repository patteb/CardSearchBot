#include <Servo.h>
#include "CardSearchBot.h"

Servo feeder_servo, sort_servo;

void setup() {
  Serial.begin(BAUDRATE);

  sort_servo.attach(SORT_PIN);
  sort_servo.write(SORT_NEUTRAL);

  pinMode(CAM_PIN, INPUT);
  pinMode(CONTAINER_PIN, INPUT);
}

void loop() {
  char incomingByte = SERIAL_NEGATIVE;
  boolean response = false;

  Serial.flush();
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    switch (incomingByte) {
      case SERIAL_FEED: //feed card
        response = feed();
        break;
      case SERIAL_QUERY: //query state of container
        response = check_empty();
        break;
      case SERIAL_MATCH: //match
        response = true;
        response = sort(true);
        break;
      case SERIAL_NO_MATCH: //no match
        response = true;
        response = sort(false);
        break;
    }
    if (response) Serial.print(SERIAL_POSITIVE);
    else Serial.print(SERIAL_NEGATIVE);
  }
}

boolean dummy() {
  if (digitalRead(CONTAINER_PIN)) return false;
  else return true;
}

boolean feed() {
  if (!(check_empty())) return false;
  else {
    feeder_servo.attach(FEED_PIN);
    feeder_servo.write(FEEDER_SPEED);
    //delay(550);//MOCKUP for CNY70-Check
    while (!(check_cam())) delay(20);
    feeder_servo.detach();
    return true;
  }
}

boolean check_empty() {
  if (digitalRead(CONTAINER_PIN)) return true;
  else return false;
}

boolean sort(boolean match) {
  if (match) sort_servo.write(SORT_MATCH);
  else sort_servo.write(SORT_CHAFF);

  while (check_cam()) delay(20);
  delay(150);
  sort_servo.write(SORT_NEUTRAL);
  return true;
}

boolean check_cam() {
  float sensorValue = 0;
  for (int i = 0; i < 10; i++) sensorValue += analogRead(CAM_PIN);
  sensorValue /= 10;
  if (sensorValue <= CNY70_LVL) return true;
  else return false;
}





