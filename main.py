import os,datetime,threading,random,time,sqlite3,csv
from flask import Flask,render_template,request,send_file
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import board
import digitalio

#DEBUG MODE
DEBUG=False
PORT=80

#BACKUP DELAY SECONDS
BACKUP_DELAY=10800 #10800 = 3 hours

app=Flask("website")
temp=0
humidite=0
battery=0
DB_NAME = 'logs.db'

print("starting hotspot : SmartComposter")
def hotspot():
    os.system('sudo nmcli device wifi hotspot ssid SmartComposter')

def log_data():
    global temp,humidite,battery
    while True:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            )
        ''')
    
        try:
            timestamp=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            cursor.execute(
                "INSERT INTO readings (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                (timestamp, temp, humidite)
            )
            conn.commit()
            print("Data logged successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            time.sleep(BACKUP_DELAY)
@app.route("/")
def main(error=None):
    global battery
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    sql_query = f"""
        SELECT * FROM readings
        ORDER BY id DESC
        LIMIT ?;
    """
    
    try:
        cursor.execute(sql_query, (10,))
        
        results = cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    sql_query = f"""
        SELECT * FROM readings
        ORDER BY id DESC
        LIMIT ?;
    """
    
    try:
        cursor.execute(sql_query, (50,))
        
        values = cursor.fetchall()
        dates= [i[1].split(" ")[0] for i in values][::-1]
        temps= [i[2] for i in values][::-1]
        humidites= [i[3] for i in values][::-1]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    ip=ni.ifaddresses('wlan0')[AF_INET][0]['addr']
    if error==None:
        return render_template("index.html",ip=ip,logs=results,battery=int(battery),dates=dates,temps=temps,humidites=humidites)
    else:
        return render_template("index.html",ip=ip,logs=results,battery=int(battery),dates=dates,temps=temps,humidites=humidites,error=error)

def radio():
    import time
    from pyrf24 import RF24, RF24_PA_HIGH,RF24_250KBPS
    global temp,humidite,battery
    # CE pin is 22, CSN pin is 8 (CE0)
    radio = RF24(22, 0) 

    def setup():
        if not radio.begin():
            print("Radio hardware not responding!")
            return False
        #MAX RANGE FOR CHANNEL 115
        radio.set_pa_level(RF24_PA_HIGH)
        radio.setChannel(115)
        radio.setDataRate(RF24_250KBPS)
        radio.open_rx_pipe(1, b"00001")
        radio.listen = True
        print("Receiver started on Channel 115...")
        return True

    if __name__ == "__main__":
        if setup():
            while True:
                if radio.available():
                    payload = radio.read(radio.getDynamicPayloadSize())
                    try:
                        data = payload.decode("utf-8").strip("\x00")
                        print(f"Received: {data}")
                        
                        if "," in data:
                            temp, humidite,battery = data.split(",")
                            print(f"-> Temp: {temp}C | Humidity: {humidite}% | Battery : {battery}%")
                    except Exception as e:
                        print(f"Decoding error: {e}")
@app.route("/logs", methods=['GET'])
def getlogfile():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    if not date1 or not date2:
        return main()
    def to_iso(date_str):
        d, m, y = date_str.split('-')
        return f"{y}-{m}-{d}"

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        start_iso = to_iso(date1)
        end_iso = to_iso(date2)
        sql_query = """
            SELECT * FROM readings 
            WHERE (substr(timestamp, 7, 4) || '-' || substr(timestamp, 4, 2) || '-' || substr(timestamp, 1, 2))
            BETWEEN ? AND ?
        """

        cursor.execute(sql_query, (start_iso, end_iso))
        results = cursor.fetchall()

        if not results:
            print(f"No records found for the range {date1} to {date2}.")
            return main(error=f"aucune mesures trouvé pour la date {date1} à {date2}.")

        else:
            print(f"Success! Found {len(results)} records.")
            
            with open('SmartComposter_logs.csv', 'w', newline='') as csvfile:
                fieldnames = ['date', 'température', 'humidité']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for res in results:
                    writer.writerow({
                        'date': res[1], 
                        'température': res[2], 
                        'humidité': res[3]
                    })
            print("Data exported to SmartComposter_logs.csv")
            return send_file("SmartComposter_logs.csv")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/temp")
def get_temp():
    global temp
    return f"{temp}"
@app.route("/humidite")
def get_humidite():
    global humidite
    return f"{humidite}"
@app.route("/poweroff")
def poweroff():
    os.system("sudo poweroff")
    main()
@app.route("/reboot")
def reboot():
    os.system("sudo reboot")
    main()

if not os.path.exists("/etc/systemd/system/website.service"):
    os.system("sudo cp website.service /etc/systemd/system")
    print("website service copied successfully !")
print("starting hotspot service !")
threading.Thread(target=hotspot).start()
print("starting logging service !") 
threading.Thread(target=log_data).start()
print("starting radio service ! ")
threading.Thread(target=radio).start()
print("starting website !")
app.run(host='0.0.0.0', port=PORT,debug=DEBUG)
