
  #define SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y 28
  #define SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X 27
  #define SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z 26


int X_MIN = 663;
int X_MAX = 375;
float X_MAP = 0;
int X_RAW = 0;
float X_G = 0;

int Y_MIN = 1007;
int Y_MAX = 1019;
float Y_MAP = 0;
int Y_RAW = 0;
float Y_G = 0;

int Z_MIN = 201;
int Z_MAX = 219;
float Z_MAP = 0;
int Z_RAW = 0;
float Z_G = 0;

float DIVISION = 1000.0;
const int samples = 10;

void setup() 
{
  Serial.begin(115200);
}


void loop() 
{

  for(int i=0;i<samples;i++)
  {
    X_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X);
    Y_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y);
    Z_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z);
  }


  X_RAW/=samples;
  Y_RAW/=samples;
  Z_RAW/=samples;

  //Convert raw values to 'milli-Gs"
  //Convert value of RawMin to -1000
  //Convert value of RawMax to 1000
  X_MAP = map(X_RAW, X_MIN, X_MAX, -DIVISION, DIVISION);
  Y_MAP = map(Y_RAW, Y_MIN, Y_MAX, -DIVISION, DIVISION);
  Z_MAP = map(Z_RAW, Z_MIN, Z_MAX, -DIVISION, DIVISION);
 
  // CALCULAR GRAVIDADE 
  X_G = X_MAP / DIVISION;
  Y_G = Y_MAP / DIVISION;
  Z_G = Z_MAP / DIVISION;

  Serial.print(X_G,0);
  Serial.print(" G");
  Serial.print("\t");

  Serial.print(Y_G,0);
  Serial.print(" G");
  Serial.print("\t");

  Serial.print(Z_G,0);
  Serial.print(" G");
  Serial.println();

  delay(200);
}