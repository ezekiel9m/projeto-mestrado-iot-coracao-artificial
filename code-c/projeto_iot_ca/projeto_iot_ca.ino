/*              UNIVERSIDADE PRESBITERIANA MACKENZIE
                PROGRAMA DE PÓS-GRADUACÃO LATU SENSO

    PROJETO DE MESTRADO EM ENGENHARIA ELÉTRICA E COMPUTAÇÃO - 2022/2024

    TEMA: INTERNET DAS COISAS E REDE MÓVEL APLICADO PARA A CRIAÇÃO DE DISPOSITIVO 
    DE MONITORAMENTO DO CORAÇÁO ARTIFICIAL COMO SOLUÇÃO DE PROBLEMA DE INSUFICENCIA CARDÍACA.

    ELABORDO POR (AUTOR): EZEQUIEL MUXIO
    ORINTADO POR: PROF. DR. CRISTIANO AKAMINE 

    ********************************** PROJETO CORAÇÃO ARTIFICIAL **********************************
    ********************* SMCA - SISTEMA DE MONITORAMENTO DO CORAÇÃO ARTIFICIAL ***************
  */
#include <Timezone.h>  
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Time.h>
#include <TimeLib.h>
#include <RTClib.h>
//#include <TinyRTClib.h>
//#include <EEPROM.h>
//#include <Ethernet.h>
#include <SPI.h>

#ifndef STASSID
  #define STASSID "@Muxito1711"
  #define STAPSK "netapta@1711"
#endif
#ifndef DEFINICAO_DE_PORTAS 
  /*PORTAS 
    26 AO
    27 A1
    28 A2
  */
  #define SENSOR_FREQ_CARDIACO_LO1 2
  #define SENSOR_FREQ_CARDIACO_LO2 3
  #define SENSOR_FREQ_CARDIACO_OUTPUT 26

  #define SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y 28
  #define SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X 27
  #define SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z 26
  #define SENSOR_MOVIMENTO_ACELEROMETRO_CS 9

  #define LED_VERDE 16
  #define LED_AMARELA 17

  #define ETHENET_TXD 18
  #define ETHENET_RXD 19

#endif

#ifndef RTC
  RTC_DS1307 rtc;
  //  char * week[7][12] = { "Domingo"      , "Segunda-feira" , "Terca-feira" ,
  //                   "Quarta-feira" , "Quinta-feira"  , "Sexta-feira" ,
  //                   "Sabado" } ;
 
    // char * month[] = { "1"  , "2" , "3"    , "4"      ,
    //                  "5"     , "6"     , "7"    , "8"     ,
    //                  "9" , "10"   , "11" , "12" } ;
  
    unsigned char buf[ 7 ] ;
    unsigned char i ;
  #define RTC_I2C_SCL 27
  #define RTC_I2C_SDA 28
#endif 
#ifndef ENDPOINTS
  const char* END_POINT_POST_CREATE = "http://127.0.0.1:8000/datas/create";
  const char* END_POINT_POST_SEND = "http://127.0.0.1:8000/notification/send_notification/5893643";
  const char* END_POINT_GET = "http://127.0.0.1:8000/network/5893643";
  const char* END_POINT_GET_DATA = "http://127.0.0.1:8000/data/data_analyse";

  HTTPClient http;
  WiFiClient client;
  int JSON_DOC_SIZE = 384;
#endif

#ifndef VARIEAVEIS 
  int DELAY = 10;
  int _LONG = 1000;
  unsigned long currentTime = millis();
  unsigned long previousTime = 0;
  const long timeoutTime = 2000;

  int SENSOR_FREQ_CARDIACO_SAIDA = 0;
  const char* IDENTIFIER = "5893643"; 
  TimeChangeRule mySTD = {"EST", First, Sun, Nov, 2, -300};    
  TimeChangeRule *tcr;   
  Timezone myTZ(mySTD);

  //Variaveis de calibracao do sensor acelerometro 
  int X_MIN = 375;
  int X_MAX = 663;
  int X_MAP = 0;
  int X_RAW = 0;
  int X_G = 0;

  int Y_MIN = 1007;
  int Y_MAX = 1019;
  int Y_MAP = 0;
  int Y_RAW = 0;
  int Y_G = 0;

  int Z_MIN = 201;
  int Z_MAX = 219;
  int Z_MAP = 0;
  int Z_RAW = 0;
  int Z_G = 0;

  float DIVISION = 1000;
  int SIMPLES = 10;
  float BATTERY = 0.0;
#endif

void starRTC(){
  BATTERY = (float (analogRead(RTC_I2C_SCL)) / float (1023) * 5); // convertendo valor análogico para ponto flutuante (numeros com virgula)
  if (BATTERY >= 2.0){
      Serial.print("Bateria em bom estado: ");
      Serial.print (BATTERY);
      Serial.println("");
    }
  else if (BATTERY < 2.0){
    Serial.print("Bateria em mal estado: ");
    Serial.print (BATTERY);
    Serial.println("");
  }
  if(rtc.begin()){
    Serial.println("RTC conectado");
     while (1);
  }
  if (! rtc.begin()) {
    Serial.println("Não foi possível encontrar o RTC");
    while (1);
  }
  else if (!rtc.isrunning()) {
    Serial.println("O RTC NÃO está funcionando!");
    // A seguinte linha define o RTC para a data e hora em que este sketch foi compilado
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}
void getNetworkConnectData() {
  if(WiFi.status()== WL_CONNECTED){
    http.useHTTP10(true);
    http.begin(END_POINT_GET_DATA);
    int httpResponseCode = http.GET();
    
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);

      String payload = http.getString();
      Serial.println(payload);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
}
void connectToWifi(){
  Serial.println("Connect to wifi");

  // StaticJsonDocument doc(2028);
  // doc = getNetworkConnectData();

  // if(doc.isNull || doc.size == 0){
  //   Serial.println("Network data not find");
  // }
  // else{
  //   // STASSID = doc["ssd"];
  //   // STAPSK =  doc["password"]
  // }
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

}
time_t compileTime()
{
    const time_t FUDGE(10);     
    const char *compDate = __DATE__, *compTime = __TIME__, *months = "JanFebMarAprMayJunJulAugSepOctNovDec";
    char chMon[4], *m;
    tmElements_t tm;

    strncpy(chMon, compDate, 3);
    chMon[3] = '\0';
    m = strstr(months, chMon);
    tm.Month = ((m - months) / 3 + 1);

    tm.Day = atoi(compDate + 4);
    tm.Year = atoi(compDate + 7) - 1970;
    tm.Hour = atoi(compTime);
    tm.Minute = atoi(compTime + 3);
    tm.Second = atoi(compTime + 6);
    time_t t = makeTime(tm);
    return t + FUDGE;           
}

String getDateTime() {
  // time_t utc = now();
  // time_t local = myTZ.toLocal(utc, &tcr);
  // delay(_LONG);

  //char date[32];
  // sprintf(date, "%.2d/%d/%d %.2d:%.2d:%.2d",
  //     day(local), month(local), year(local), hour(local), minute(local), second(local));
  // //Serial.println(date);

  DateTime now = rtc.now();
  char dateNow[32];
  //String dateNow = now.day()+"/"+now.month()"/"+now.year()+" "+":"+now.hour()+":"+now.minute()+":"+now.second();
  sprintf(dateNow, "%.2d/%d/%d %.2d:%.2d:%.2d",
    now.day(), now.month(), now.year(), now.hour(), now.minute(), now.second());

  return String(dateNow);
}
void connectEthernet(){
  /*while (!Serial) continue;

  // Initialize Ethernet library
  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
  if (!Ethernet.begin(mac)) {
    Serial.println(F("Failed to configure Ethernet"));
    return;
  }
  delay(_LONG);

  Serial.println(F("Connecting..."));

  // Connect to HTTP server
  EthernetClient client;
  client.setTimeout(10000);
  if (!client.connect(END_POINT_POST_CREATE, 80)) {
    Serial.println(F("Connection failed"));
    return;
  }

  Serial.println(F("Connected!"));
  */
}
void collectSensorsData(){
  digitalWrite(LED_AMARELA, HIGH);  
  delay(_LONG);                      
  digitalWrite(LED_AMARELA, LOW);   
  delay(_LONG);

  // Letira dos dados do sensor de batimento cardiáco 
  if((digitalRead(SENSOR_FREQ_CARDIACO_LO1) != 1)||(digitalRead(SENSOR_FREQ_CARDIACO_LO2) != 1)){
    SENSOR_FREQ_CARDIACO_SAIDA = analogRead(SENSOR_FREQ_CARDIACO_OUTPUT);
    Serial.print(SENSOR_FREQ_CARDIACO_SAIDA);
    //Serial.println();
  }
  delay(DELAY);

  // Leitura dos dados do sensor acerelometro 
  for(int i=0; i<SIMPLES; i++)
  {
    X_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X);
    Y_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y);
    Z_RAW +=analogRead(SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z);
  }

  X_RAW/=SIMPLES;
  Y_RAW/=SIMPLES;
  Z_RAW/=SIMPLES;

  //Calibração dos dados do sensor de movimento e gravida (Acelerômetro)
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

  JsonDocument doc;
  JsonObject datas = doc.as<JsonObject>();
  JsonObject data = doc.as<JsonObject>();
  JsonObject movimets = doc.as<JsonObject>();
  JsonArray body = doc.to<JsonArray>();

  //DynamicJsonDocument doc(JSON_DOC_SIZE);
  //JsonObject datas = doc.createNestedObject("datas");
  //JsonObject data = doc.createNestedObject("data");
  //JsonArray body = doc.createNestedArray("body");
  //JsonObject movimets = doc.createNestedObject("movimets");

  datas["identifier"] = IDENTIFIER;

  movimets["X"] = X_G;
  movimets["Y"] = Y_G;
  movimets["Z"] = Z_G;

  data["movimets"] = movimets;
  data["heartbeat"] = SENSOR_FREQ_CARDIACO_SAIDA;
  //data["datecollect"] = getDateTime();
  data["location"] = "";
  body.add(data);
  
  datas["body"] = body;
 
  //serializeJson(doc, Serial);
  serializeJsonPretty(datas, Serial);

  // if ((currentTime - previousTime) > timeoutTime) {
  //   send_data(datas);
  // }
  //previousTime = millis();
  //sendData(String(datas));
}

void sendData(String jsonData){

  if ((WiFi.status() == WL_CONNECTED)) {
    Serial.println("");
    Serial.print("Connected! IP address: ");
    Serial.println(WiFi.localIP());

    http.setInsecure();

    http.begin(client, END_POINT_POST_CREATE);
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] POST... code: %d\n", httpResponseCode);

      if (int(httpResponseCode) == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }
  else{
    Serial.println("Network is not connected!");
  }
  delay(_LONG);
  // if(WiFi.status()== WL_CONNECTED){
  //     WiFiClient client;
  //     HTTPClient http;
    
  //     http.begin(client, END_POINT_POST_CREATE);
  
  //     http.addHeader("Content-Type", "application/json");
  //     int httpResponseCode = http.POST(String(Data));
     
  //     Serial.print("HTTP Response code: ");
  //     Serial.println(httpResponseCode);
        
  //     // Free resources
  //     http.end();
  //   }
  //   else {
  //     Serial.println("WiFi Disconnected");
  //   }
  // }
}
void leds(){
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(_LONG);                      
  digitalWrite(LED_BUILTIN, LOW);   
  delay(_LONG);

  digitalWrite(LED_VERDE, HIGH);  
  delay(_LONG);                      
  digitalWrite(LED_VERDE, LOW);   
  delay(_LONG);
}
void setup() {
  Serial.begin(115200);
  starRTC();
  //setTime(myTZ.toUTC(compileTime()));

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELA, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(SENSOR_FREQ_CARDIACO_LO1, INPUT); 
  pinMode(SENSOR_FREQ_CARDIACO_LO2, INPUT); 
  pinMode(SENSOR_FREQ_CARDIACO_OUTPUT, OUTPUT); 
  pinMode(SENSOR_MOVIMENTO_ACELEROMETRO_LCS_X, INPUT); 
  pinMode(SENSOR_MOVIMENTO_ACELEROMETRO_SDA_Y, INPUT); 
  pinMode(SENSOR_MOVIMENTO_ACELEROMETRO_SDO_Z, INPUT); 

  connectToWifi();
  //connectEthernet();
}

void loop() {
  leds();
  collectSensorsData();
  getNetworkConnectData();
  
}
