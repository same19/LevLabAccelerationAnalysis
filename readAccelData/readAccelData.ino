void setup() {
  Serial.begin(4000000);
}
void loop() {
  Serial.println(analogRead(A0));
}
