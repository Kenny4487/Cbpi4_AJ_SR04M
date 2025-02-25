# craftbeerpi4-SR04M-Ultrasonic sensor

Craftbeerpi Sensors for using SR04 ultrasonic sensor modules. It should work with most SR04 sensors, but I only tested AJ-SR04M.

The Plugin comes with two sensors:
- SR04M distance
- SR04M volume
The distance sensor just returns the measured distance (in cm).
The volume sensor has "pot diameter" and "mounting height" as parameters to calculate the filled volume (in liters).

RaspberryPi GPIO operate with 3.3V, but many SR04M modules operate with 5V.
To make it safe to use I used an external 5V power supply and then connected the trigger pin directly to the Raspberry GPIO.
For the echo pin I used a 330 Ohm resistor between the SR04M module and the RPi and an additional 10k pulldown resistor to GND.

So far Flowstep usage has not been implemented, it's just a basic sensor and my first RPi programming experience.
