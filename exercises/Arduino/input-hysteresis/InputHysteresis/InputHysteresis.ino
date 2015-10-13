// InputHysteresis.ino : Arduino program to demonstrate a simple single-state hysteretic response.

// Copyright (c) 2014-2015, Garth Zeglin.  All rights reserved. Licensed under the terms
// of the BSD 3-clause license as included in LICENSE.

// The baud rate is the number of bits per second transmitted over the serial port.
#define BAUD_RATE 115200

// This assumes a photoresistor is pulling A0 up and a resistor is pulling A0
// down.  When the input is bright, the voltage increases, when dark, the
// voltage decreases.
#define INPUT_PIN A0

// Some version of the Arduino IDE don't correctly define this symbol for an
// Arduino Uno.
#ifndef LED_BUILTIN
#define LED_BUILTIN 13
#endif

/****************************************************************/
// Global variables.

// The state of the system can be captured with only two values, e.g., it is
// represented as a single bit.  The following statement defines two symbolic
// values, one for each possible state.
enum state_t { WAITING_FOR_LIGHT, WAITING_FOR_DARK };

// Declare the state variable as a symbolic value.
enum state_t state = WAITING_FOR_LIGHT;

// The hysteretic response is defined by using two thresholds.  
const int light_threshold = 700;
const int dark_threshold  = 300;

/****************************************************************/
/**** Standard entry points for Arduino system ******************/
/****************************************************************/

// Standard Arduino initialization function to configure the system.

void setup()
{
  // initialize the Serial port
  Serial.begin( BAUD_RATE );

  // configure our trivial I/O
  pinMode( LED_BUILTIN, OUTPUT );

  // the LED start out ON to match the initial state
  digitalWrite(LED_BUILTIN, HIGH);
}

/****************************************************************/
// Standard Arduino polling function.

void loop()
{
  // Read the ambient light level.
  int input = analogRead(INPUT_PIN);

  if (state == WAITING_FOR_DARK) {
    if (input < dark_threshold) {
      Serial.print("Dark observed at input level ");
      Serial.println(input);
      Serial.println("Transitioning to the WAITING_FOR_LIGHT state.");
      
      state = WAITING_FOR_LIGHT;
      digitalWrite(LED_BUILTIN, HIGH);
    }

  } else { // state must be WAITING_FOR_LIGHT
    if (input > light_threshold) {
      Serial.print("Light observed at input level ");
      Serial.println(input);
      Serial.println("Transitioning to the WAITING_FOR_DARK state.");
      
      state = WAITING_FOR_DARK;
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}

/****************************************************************/
