const int analogInPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(analogInPin);

  float voltage = sensorValue / (42.2);

    Serial.print("Voltage: ");
    Serial.print(voltage);
    Serial.println(" V");


  delay(5000);
}
