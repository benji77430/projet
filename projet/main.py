import os,datetime,threading,time
from flask import Flask,render_template
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
DEBUG=False
temp=""
app=Flask("website")
def radio():
    global temp
    from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS

    # Pinout for Raspberry Pi
    CE_PIN = 22  # GPIO 22
    CSN_PIN = 0  # SPI0 CE0
    radio = RF24(CE_PIN, CSN_PIN)

    # Must match the Arduino address
    address = b'00001'

    def setup():
        radio.begin()
        radio.openReadingPipe(1, address)        # Reading pipe 1
        radio.setPALevel(RF24_PA_MAX)           # RF24_PA_MIN, LOW, HIGH, MAX
        radio.setDataRate(RF24_250KBPS)         # 250KBPS = longer range
        radio.setChannel(80)                     # Same channel as Arduino
        radio.startListening()                   # Set as receiver
        print("Radio initialized, waiting for payload...")

    setup()
    while True:
        if radio.available():
            # Create a buffer of max 32 bytes (nRF24L01 max payload)
            received_payload = radio.read(radio.getDynamicPayloadSize())
            # Decode to string and strip null terminator
            payload = received_payload.decode('utf-8').rstrip('\x00')
            print(f"Received: {payload}")
            try:
                temp=payload.split(",")[0]
                humidite=payload.split(",")[1]
            except Exception as e:
                print(f"an error as occured : {e}")
        time.sleep(0.01)  # small delay
@app.route("/")
def main():
    ip =ni.ifaddresses('wlan0')[AF_INET][0]['addr']
    return render_template("index.html",ip=ip)

@app.route('/get-live-data')
def get_live_data():
    global temp
    heure=datetime.datetime.now()
    h=heure.hour
    m=heure.minute
    s=heure.second
    return f"""
<p>Température : {temp}<br><br>
Time : {h} : {m} : {s}
</p>
    """
threading.Thread(target=radio).start()
app.run(host='0.0.0.0', port=80,debug=DEBUG)