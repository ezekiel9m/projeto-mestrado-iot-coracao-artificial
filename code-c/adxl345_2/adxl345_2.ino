#include <Wire.h>  
int ADXL345 = 0x53; 
int X, Y, Z, T;  
int DIVISOR = 256;


#define SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y 28
#define SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X 27
#define SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z 26
#define SENSOR_MOVIMENTO_ACELEROMETRO_CS 9

void setup() {
  Serial.begin(9600); 
  delay(10);
}
void loop() {
  X = analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X) << 8; 
  Y = analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y) << 8; 
  Z = analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z) << 8; 
  T = analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_CS);

  X = X/DIVISOR; 
  Y = Y/DIVISOR;
  Z = Z/DIVISOR;

  Serial.print("X= ");
  Serial.print(X);

  Serial.print("   Y= ");
  Serial.print(Y);

  Serial.print("   Z= ");
  Serial.println(Z);

  Serial.println();
  Serial.print("   T= ");
  Serial.println(T);
}