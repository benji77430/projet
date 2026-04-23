#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "DFRobot_SHT20.h"
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define i2c_Address 0x3c

Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
DFRobot_SHT20 sht20;

    RF24 radio(10,9); // CE, CSN
    const byte address[6] = "00001";
    float temp,hum = 0;
    int batterie = 100;

void setup() {
  display.begin(i2c_Address, true);
  sht20.initSHT20();
  
  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.drawRect(0, 0, 128, 64, SH110X_WHITE);
  display.drawRect(2, 2, 124, 60, SH110X_WHITE);
  display.setTextSize(2); 
  display.setCursor(35, 15);
  display.print("SMART");
  display.drawLine(30, 33, 98, 33, SH110X_WHITE);
  display.setTextSize(1);
  display.setCursor(35, 38); 
  display.print("COMPOSTEUR");
  display.display();
  
  delay(3000); 

      Serial.begin(9600);
      radio.begin();
      radio.openWritingPipe(address);
      radio.setPALevel(RF24_PA_MAX); 
      radio.setDataRate(RF24_250KBPS);
      radio.setChannel(115); 
      radio.stopListening();
}

    void send_radio_data() {
      String text = String(int(temp*10))+","+String(int(hum*10))+","+String(int(batterie));
      Serial.print("Sending : ");
      Serial.println(text);
      radio.write(text.c_str(), text.length());
    }

void loop() {
  send_radio_data();
  temp = sht20.readTemperature();
  hum = sht20.readHumidity();
  

  display.clearDisplay();
  
  display.setTextSize(1);
  display.setCursor(5, 2);
  display.print("STATUT");
  
  display.setCursor(90, 2);
  display.print(batterie);
  display.print("%");
  display.drawRect(115, 1, 12, 7, SH110X_WHITE);
  display.drawPixel(127, 3, SH110X_WHITE);
  display.drawPixel(127, 4, SH110X_WHITE);

  display.drawLine(0, 12, 128, 12, SH110X_WHITE);

  display.setCursor(10, 20);
  display.setTextSize(1);
  display.print("Temperature:");
  display.setCursor(15, 32);
  display.setTextSize(2);
  display.print(temp, 1);
  display.print(" C");

  display.setTextSize(1);
  display.setCursor(10, 52);
  display.print("Humidite: ");
  display.print(hum, 1);
  display.print("%");

  display.display();
  delay(500);
}