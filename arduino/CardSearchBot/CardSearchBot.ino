#include <Servo.h>
#include "CardSearchBot.h"

Servo feeder_servo, sort_servo;

void setup() {
  Serial.begin(BAUDRATE);

  feeder_servo.attach(FEED_PIN);
  sort_servo.attach(SORT_PIN);

  pinMode(CAM_PIN, INPUT);
  pinMode(CONTAINER_PIN, INPUT);

  pinMode(13, OUTPUT);
  pinMode(2, INPUT);
}

void loop() {
  char incomingByte = SERIAL_NEGATIVE;
  boolean response = false;

  Serial.flush();
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    switch (incomingByte) {
      case SERIAL_FEED: //feed card
        response = true;
        break;
      case SERIAL_QUERY: //query state of container
        response = dummy();
        break;
      case SERIAL_MATCH: //match
        response = true;
        break;
      case SERIAL_NO_MATCH: //no match
        response = true;
        break;
    }
    if (response) Serial.print(SERIAL_POSITIVE);
    else Serial.print(SERIAL_NEGATIVE);
  }
}

boolean dummy() {
  if (digitalRead(2)) return true;
  else return false;
}



