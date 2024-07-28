#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Bounce2.h>

const int sensorPin = 11; // Sensor Pin
int num = 5;
float zeroDistance = 0.0;
float Mdistance;
unsigned long startTime;
bool zeroSet = false;
bool dataCollectionActive = true; // Variable to control the collect data
bool end = false; // End code

// Button Pin
const int buttonPin = 2;

// LCD's definition
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Inicialize the object "bounce" for button
Bounce debouncer = Bounce();

void setup() {
  // LCD Inicialize
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Dist:");
  lcd.setCursor(0, 1);
  lcd.print("Tempo:");
  
  Serial.begin(9600);
  
  pinMode(buttonPin, INPUT_PULLUP);
  debouncer.attach(buttonPin);
  debouncer.interval(50); // debounce interval
  
  startTime = millis(); // counting time

  Serial.println("=============================");
  Serial.println("            START            ");
  Serial.println("=============================");
}

void loop() {
  // update the button state
  debouncer.update();
  
  // verify if has passed 20 seconds from the start
  if (millis() - startTime > 20000) {
    dataCollectionActive = false;
    
    if(end==false){
      Serial.println("=============================");
      Serial.println("             END             ");
      Serial.println("=============================");
      end = true;
    }
  }

  // Verify if the button has pressed for reset time and define a zero point 
    if (debouncer.fell()) {
      lcd.clear();
      zeroDistance = Mdistance;
      zeroSet = true;
      lcd.setCursor(0, 0);
      lcd.print("Dist Inicial:");
      lcd.setCursor(0, 1);
      lcd.print(zeroDistance, 2);
      lcd.print(" cm");
      delay(500);
  
      // wait for the second press for the button 
      unsigned long pressStartTime = millis();
      while (millis() - pressStartTime < 2000) {
        debouncer.update();
        if (debouncer.fell()) {
          zeroSet = false;
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Dist Inicial:");
          lcd.setCursor(0, 1);
          lcd.print("0.0 cm");
          delay(500);
          break;
        }
      }
  
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Dist:");
      lcd.setCursor(0, 1);
      lcd.print("Tempo:");
      dataCollectionActive = true;
      end = false;
      Serial.println("=============================");
      Serial.println("            START            ");
      Serial.println("=============================");
      startTime = millis(); // restart the time
    }
  
  // Executa apenas se a coleta de dados estiver ativa
  if (dataCollectionActive) {
    // Distancia media
    Mdistance = calcularMediaPulsos(num); 
    
    // Ajustar a distância com base no ponto zero
    float adjustedDistance = zeroSet ? Mdistance - zeroDistance : Mdistance;
  
    // Tempo em milissegundos desde o start do programa ou desde o last reset
    unsigned long currentTime = millis() - startTime;
    
    // Exibir dados no LCD
    lcd.setCursor(6, 0);
    lcd.print(adjustedDistance, 2); // Mostra a distance ajustada com duas casas decimais
    lcd.print(" cm   "); // Espaços extras para limpar dados antigos
    lcd.setCursor(7, 1);
    lcd.print(currentTime / 1000.0, 2); // Tempo em segundos com duas casas decimais
    lcd.print(" s   ");
    
    // Enviar dados via serial para coleta externa
    Serial.print(adjustedDistance, 2);
    Serial.print(", ");
    Serial.println(currentTime / 1000.0, 2);
  }
  
  // Pequeno atraso para evitar sobrecarga
  delay(10);
}

float calcularMediaPulsos(int numPulsos) {
  float totalDistancia = 0.0;
  int sensorValue;
  
  // Realiza a leitura dos pulsos e acumula o total
  for (int i = 0; i < numPulsos; ++i) {
    sensorValue = pulseIn(sensorPin, HIGH);
    
    // Calcular a distance usando a formule fornecida
    float distanceInMm = (3.0 / 4.0) * (sensorValue - 1000);
    float distance = distanceInMm / 10.0; // Convertendo de mm para cm
    totalDistancia += distance;
  }
  
  // Calculate the media distance 
  float mediaDistancia = totalDistancia / numPulsos;
  
  return mediaDistancia;
