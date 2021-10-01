#include "LowPower.h"

/**********************
 * User Configuration *
 **********************/ 
// Time between two samples from the Raspberry Pi
unsigned int SLEEP_TIME = 1;  // minutes
// Maximum number of samples from Raspberry Pi
unsigned int MAX_N_SAMPLES = 65535;
// Enable serial debug by uncommenting the line below
#define DEBUG


/***********************
 * Internal Variabiles *
 ***********************/
// Pinout specific to hardware configuration (Minion Teach Hardware 1606696)
int PIN_PI_ON = 3;
int PIN_PI_OFF = 2;
int PIN_WIFI = 12;
int PIN_OVER = 13;  // same as BUILTIN_LED

bool RECOVER = false;
unsigned int SAMPLE_COUNT = 0;
unsigned int SLEEP_REV = SLEEP_TIME*15;


void setup(void)
{
  #ifdef DEBUG  
  Serial.begin(9600);
  Serial.println("MINION SETUP");
  Serial.print("PIN_PI_ON: "); Serial.println(PIN_PI_ON);
  Serial.print("PIN_PI_OFF: "); Serial.println(PIN_PI_OFF);
  Serial.print("PIN_WIFI: "); Serial.println(PIN_WIFI);
  Serial.print("PIN_OVER: "); Serial.println(PIN_OVER);
  Serial.print("SLEEP_TIME: "); Serial.println(SLEEP_TIME);
  Serial.print("MAX_N_SAMPLES: "); Serial.println(MAX_N_SAMPLES);
  Serial.println();
  Serial.flush();
  #endif

  // Set pinout
  pinMode(PIN_WIFI, INPUT_PULLUP);
  pinMode(PIN_OVER, INPUT_PULLUP);
  pinMode(PIN_PI_ON, OUTPUT);
  pinMode(PIN_PI_OFF, OUTPUT);

  // Power off Pi
  digitalWrite(PIN_PI_ON, LOW);
  digitalWrite(PIN_PI_OFF, HIGH);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
  digitalWrite(PIN_PI_OFF, LOW);
}


void sample() {
  // Power on Pi and wait 64 seconds for Pi to boot
  #ifdef DEBUG
  Serial.println("Pi ON"); Serial.flush();
  #endif
  digitalWrite(PIN_PI_ON, HIGH);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
  digitalWrite(PIN_PI_ON, LOW);
  for(unsigned int i = 0; i < 8; i++) {
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  }
  
  // Check Pi status every second
  int wifi_status = digitalRead(PIN_WIFI);
  int over_status = digitalRead(PIN_OVER);
  do {
    LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
    wifi_status = digitalRead(PIN_WIFI);
    over_status = digitalRead(PIN_OVER);
    if (over_status == LOW){ RECOVER = true; }
    else { RECOVER = false; }
    #ifdef DEBUG
    Serial.print("WIFI STATUS:"); Serial.print(wifi_status);
    Serial.print("   OVER STATUS:"); Serial.println(over_status);
    Serial.flush();
    #endif
  } while (wifi_status == HIGH);

  // Wait 20 seconds for Pi to shutdown and turn power off to Pi
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  #ifdef DEBUG
  Serial.println("Pi OFF"); Serial.flush();
  #endif
  digitalWrite(PIN_PI_OFF, HIGH);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
  digitalWrite(PIN_PI_OFF, LOW);
}


void loop(void) 
{
  // Sample with Pi
  #ifdef DEBUG  
  Serial.println("Pi Sample"); Serial.flush();
  #endif
  sample();
  SAMPLE_COUNT = SAMPLE_COUNT + 1;

  // Sleep forever before recovery
  if (RECOVER == true || SAMPLE_COUNT > MAX_N_SAMPLES) {
    #ifdef DEBUG  
    Serial.println("Sleep forever"); Serial.flush();
    #endif
    LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
  }

  // Sleep in between picture burst
  #ifdef DEBUG    
  Serial.print("Sleep"); Serial.flush();
  #endif
  //This is the sleep cycle! Set for 150 cycles of 4 seconds for 10 minutes
  for(unsigned int i = 0; i < SLEEP_REV; i++) {
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }
}
