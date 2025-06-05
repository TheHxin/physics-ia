/* DS18B20 1-Wire digital temperature sensor with Arduino example code. More info: https://www.makerguides.com */

// Include the required Arduino libraries:
#include "OneWire.h"
#include "DallasTemperature.h"

// Define to which pin of the Arduino the 1-Wire bus is connected:
#define ONE_WIRE_BUS_1 10
#define ONE_WIRE_BUS_2 9
#define ONE_WIRE_BUS_3 8

// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire_1(ONE_WIRE_BUS_1);
OneWire oneWire_2(ONE_WIRE_BUS_2);
OneWire oneWire_3(ONE_WIRE_BUS_3);
// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensor_1(&oneWire_1);
DallasTemperature sensor_2(&oneWire_2);
DallasTemperature sensor_3(&oneWire_3);

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
  // Start up the library:
  sensor_1.setResolution(9);
  sensor_2.setResolution(9);
  sensor_3.setResolution(9);

  sensor_1.begin();
  sensor_2.begin();
  sensor_3.begin();
}

void loop() {
  // Send the command for all devices on the bus to perform a temperature conversion:
  sensor_1.requestTemperatures();
  sensor_2.requestTemperatures();
  sensor_3.requestTemperatures();

  // Fetch the temperature in degrees Celsius for device index:
  float tempC_1 = sensor_1.getTempCByIndex(0); // the index 0 refers to the first device
  float tempC_2 = sensor_2.getTempCByIndex(0); // the index 0 refers to the first device
  float tempC_3 = sensor_3.getTempCByIndex(0); // the index 0 refers to the first device
  // Fetch the temperature in degrees Fahrenheit for device index:

  // Print the temperature in Celsius in the Serial Monitor:
  //Serial.print("Temperature: ");
  //Serial.print(tempC_1);
  //Serial.print(" \xC2\xB0"); // shows degree symbol
  //Serial.println("C");

  //Serial.print("Temperature: ");
  //Serial.print(tempC_2);
  //Serial.print(" \xC2\xB0"); // shows degree symbol
  //Serial.println("C");

  //Serial.print("Temperature: ");
  //Serial.print(tempC_3);
  //Serial.print(" \xC2\xB0"); // shows degree symbol
  //Serial.println("C");

  //Serial.println("----------------------------");

  Serial.print(tempC_1);
  Serial.print(",");
  Serial.print(tempC_2);
  Serial.print(",");
  Serial.println(tempC_3);
  // Wait 1 second:
  delay(100);
}