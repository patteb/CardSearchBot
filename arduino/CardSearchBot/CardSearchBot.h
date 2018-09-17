//PINOUT is a mockup
#define FEED_PIN 1
#define SORT_PIN 2
#define CAM_PIN 3
#define CONTAINER_PIN 4

#define BAUDRATE 115200
#define CNY70_LVL 512

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

#define SERIAL_FEED 'f'
#define SERIAL_QUERY 'q'
#define SERIAL_MATCH 'm'
#define SERIAL_NO_MATCH 'c'
#define SERIAL_NEGATIVE 'n'
#define SERIAL_POSITIVE 'y'
 
