#include "LowPower.h"

int Pi_on = 3;
int Pi_off = 2;
int WIFI_SIG = 4;
int IO = 5;
int LED = 13;

int RECOVER = 0;
int SAMPLES = 0;
int Sample_Num = 30000;

///////////////////////////////////
// Sleep cycle in minutes
int sleepTime = 15;
///////////////////////////////////

int sleepRev = sleepTime*15;

void setup(void)
{
  pinMode(WIFI_SIG, INPUT_PULLUP);
  pinMode(Pi_on, OUTPUT); 
  pinMode(IO, INPUT_PULLUP);
  pinMode(Pi_off, OUTPUT);

  digitalWrite(Pi_on, LOW);
  digitalWrite(Pi_off, HIGH);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
  digitalWrite(Pi_off, LOW);
  digitalWrite(LED, LOW);

  for(int i = 0; i < 3; i++){
    digitalWrite(LED, HIGH);
    delay(400);
    digitalWrite(LED, LOW);
    delay(100);
  }
}

void Pi_Samp() {
  digitalWrite(Pi_on, HIGH);
  LowPower.powerDown(SLEEP_2S, ADC_OFF, BOD_OFF);
  digitalWrite(Pi_on, LOW);

  for (int i = 1; i <= 12; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  int WIFI_Status = digitalRead(WIFI_SIG);
  int Press_Status = digitalRead(IO);

  do {
    digitalWrite(LED, HIGH);
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
    WIFI_Status = digitalRead(WIFI_SIG);
    Press_Status = digitalRead(IO);
    if (Press_Status == LOW){
      RECOVER = 1;
    }
  }
  while (WIFI_Status == HIGH);

  digitalWrite(LED, LOW);

  for (int i = 1; i <= 5; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

  digitalWrite(Pi_off, HIGH);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
  digitalWrite(Pi_off, LOW);
}

void Pi_Samp_RECOVER() {

  for (int i = 1; i <= 10000; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }


}

void loop(void) 
{

  Pi_Samp();

  SAMPLES = SAMPLES + 1;

  if (RECOVER == 1 || SAMPLES > Sample_Num) {
    RECOVER = 0;
    while(1) {
      Pi_Samp_RECOVER();
    }
  }
  //This is the sleep cycle! Set for 150 cycles of 4 seconds for 10 minutes
  for (int i = 1; i <= sleepRev; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }

}







