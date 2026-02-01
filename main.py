import os,datetime,threading,time
from flask import Flask,render_template

DEBUG=False
message=""
app=Flask("website")
def radio():
    global message
    from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS

    # Pinout for Raspberry Pi
    CE_PIN = 25  # GPIO 22
    CSN_PIN = 0  # SPI0 CE0
    radio = RF24(CE_PIN, CSN_PIN)

    # Must match the Arduino address
    address = b'00001'

    def setup():
        radio.begin()
        radio.openReadingPipe(1, address)        # Reading pipe 1
        radio.setPALevel(RF24_PA_MIN)           # RF24_PA_MIN, LOW, HIGH, MAX
        radio.setDataRate(RF24_250KBPS)         # 250KBPS = longer range
        radio.setChannel(80)                     # Same channel as Arduino
        radio.startListening()                   # Set as receiver
        print("Radio initialized, waiting for messages...")

    setup()
    while True:
        if radio.available():
            # Create a buffer of max 32 bytes (nRF24L01 max payload)
            received_payload = radio.read(radio.getDynamicPayloadSize())
            # Decode to string and strip null terminator
            message = received_payload.decode('utf-8').rstrip('\x00')
            print(f"Received: {message}")
        time.sleep(0.01)  # small delay
@app.route("/")
def main():
    
    return render_template("index.html")

@app.route('/get-live-data')
def get_live_data():
    global message
    heure=datetime.datetime.now()
    h=heure.hour
    m=heure.minute
    s=heure.second
    return f"""
<p>Méssage : {message}<br><br>
Time : {h} : {m} : {s}
</p>
    """
threading.Thread(target=radio).start()
app.run(host='0.0.0.0', port=80,debug=DEBUG)