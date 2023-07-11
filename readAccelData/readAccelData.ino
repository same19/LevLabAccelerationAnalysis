void setup() {
  Serial.begin(4000000); //115200
}
void loop() {
  Serial.println(analogRead(A0));
}
