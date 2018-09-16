#include <Servo.h>

//PINOUT is a mockup
#define FEED 1
#define SORT 2
#define DETECT 3

#define BAUDRATE 115200

void setup() {
  Serial.begin(BAUDRATE);
  pinMode(13, OUTPUT);
  pinMode(2, INPUT);
}

void loop() {
  char incomingByte = 'n';
  boolean response = false;
  /* 1-char codes for communication
  ** -----------------------------------
  ** sym - dir - translation
  ** -----------------------------------
  ** f - in - feed new card
  ** q - in - query state of container
  ** m - in - match
  ** c - in - no match ("chaff")
  ** n - out - negative confirmation
  ** y - out - positive confirmation
  */
  Serial.flush();
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    switch (incomingByte) {
      case 'f': //feed card
        response = true;
        break;
      case 'q': //query state of container
        response = dummy();
        break;
      case 'm': //match
        response = true;
        break;
      case 'c': //no match
        response = true;
        break;
    }
    if (response) Serial.print('y');
    else Serial.print('n');
  }
}

boolean dummy() {
  if (digitalRead(2)) return true;
  else return false;
}



