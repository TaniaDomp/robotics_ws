const int joyX = 35; // Pin VRx en GPIO 15
const int joyY = 34;  // Pin VRy en GPIO 2

int xValue = 0;
int yValue = 0;

void setup() {
  Serial.begin(115200); // 115200 baudios es la velocidad estándar para la ESP32
}

void loop() {
  xValue = analogRead(joyX);
  yValue = analogRead(joyY);

  // Muestra los valores (0 a 4095) separados por una tabulación
  Serial.print(xValue);
  Serial.print("\t");
  Serial.println(yValue);

  delay(50); // Pequeña pausa para no saturar el puerto serie
}