void collectSensorsData(){ 
  // Letira dos dados do sensor de batimento cardiaco 
  if((digitalRead(SENSOR_FREQ_CARDIACO_LO1) != 1)||
  (digitalRead(SENSOR_FREQ_CARDIACO_LO2) != 1)){
    SENSOR_FREQ_CARDIACO_SAIDA =
    analogRead(SENSOR_FREQ_CARDIACO_OUTPUT);
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

  /*Calibração dos dados do sensor de 
  movimento e gravida (Acelerômetro)*/
  
  X_MAP = map(X_RAW, X_MIN, X_MAX, -DIVISION, DIVISION);
  Y_MAP = map(Y_RAW, Y_MIN, Y_MAX, -DIVISION, DIVISION);
  Z_MAP = map(Z_RAW, Z_MIN, Z_MAX, -DIVISION, DIVISION);
 
  // CALCULAR GRAVIDADE 
  X_G = X_MAP / DIVISION;
  Y_G = Y_MAP / DIVISION;
  Z_G = Z_MAP / DIVISION;

  DynamicJsonDocument doc(JSON_DOC_SIZE);
  JsonObject datas = doc.createNestedObject("datas");
  JsonObject data = doc.createNestedObject("data");
  JsonArray body = doc.createNestedArray("body");
  JsonObject movimets = doc.createNestedObject("movimets");

  datas["identifier"] = IDENTIFIER;

  movimets["X"] = X_G;
  movimets["Y"] = Y_G;
  movimets["Z"] = Z_G;

  data["movimets"] = movimets;
  data["heartbeat"] = SENSOR_FREQ_CARDIACO_SAIDA;
  data["datecollect"] = getDateTime();
  data["location"] = getLocation();
  body.add(data);
  
  datas["body"] = body;
 
  //serializeJson(doc, Serial);
  serializeJsonPretty(datas, Serial);

  if ((currentTime - previousTime) > timeoutTime) {
    sendData(datas);
  }
  previousTime = millis();
}

//Nota: Os códigos completos estão em: sketch-iot-ca/projeto_iot_ca.ino