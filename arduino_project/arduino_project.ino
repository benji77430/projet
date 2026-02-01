    #include <SPI.h>
    #include <nRF24L01.h>
    #include <RF24.h>
    RF24 radio(9,10); // CE, CSN
    int temp=0;
    const byte address[6] = "00001";
    void setup() {
      Serial.begin(9600);
      radio.begin();
      radio.openWritingPipe(address);
      radio.setPALevel(RF24_PA_MAX); //can set: RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
      radio.setDataRate(RF24_250KBPS); //set as: F24_250KBPS, F24_1MBPS, F24_2MBPS ==>250KBPS = longest range
      radio.setChannel(80); //sets channel from 2.4 to 2.524 GHz in 1 MHz increments 2.483.5 GHz is normal legal limit
      radio.stopListening();
    }
    void send_radio_data() {
      String text = String(temp)+",98";
      temp++;
      Serial.print("Sending : ");
      Serial.println(text);
      radio.write(text.c_str(), text.length() + 1);
    }
    void loop() {
      send_radio_data();
      
      delay(500);
      
    }