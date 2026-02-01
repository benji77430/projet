import time
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
                print(f"Température : {temp}")
            except Exception as e:
                print(f"an error as occured : {e}")
        time.sleep(0.01)  # small delay
radio()