import os,datetime,threading,random,time,sqlite3
from flask import Flask,render_template,request
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
#DEBUG MODE
DEBUG=False

#BACKUP DELAY SECONDS
BACKUP_DELAY=600

app=Flask("website")
temp=0
humidite=0
battery=0
DB_NAME = 'logs.db'
def log_data():
    global temp,humidite,battery
    while True:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            )
        ''')
    
        # Insert the new data
    
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
            time.sleep(10800)
@app.route("/")
def main():
    global battery
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # THE KEY SQL QUERY EXPLANATION:
    # 1. ORDER BY id DESC: Sorts the entire table by ID in DESCENDING order. 
    #    This puts the highest (newest) IDs at the top.
    # 2. LIMIT N: Restricts the result set to only the top N rows.
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
        dates= [i[1] for i in values]
        temps= [i[2] for i in values]
        humidites= [i[3] for i in values]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    ip=ni.ifaddresses('wlan0')[AF_INET][0]['addr']
    
    return render_template("index.html",ip=ip,logs=results,battery=int(battery),dates=dates,temps=temps,humidites=humidites)

def radio():
    import time
    global temp,humidite,battery
    temp=float(random.randint(-100,1400))/10
    humidite=float(random.randint(0,1000,))/10
    battery=float(random.randint(0,1000))/10
@app.route("/logs", methods=['GET'])
def getlogfile():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    if not date1 or not date2:
        main()
    def to_iso(date_str):
        d, m, y = date_str.split('-')
        return f"{y}-{m}-{d}"

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()


        # Conversion for the SQL placeholders
        start_iso = to_iso(date1)
        end_iso = to_iso(date2)

        # The Logic:
        # 1. substr(timestamp, 1, 10) grabs just the "DD-MM-YYYY" part.
        # 2. We rearrange it to YYYY-MM-DD so the 'BETWEEN' comparison actually works.
        sql_query = """
            SELECT * FROM readings 
            WHERE (substr(timestamp, 7, 4) || '-' || substr(timestamp, 4, 2) || '-' || substr(timestamp, 1, 2))
            BETWEEN ? AND ?
        """

        cursor.execute(sql_query, (start_iso, end_iso))
        results = cursor.fetchall()

        if not results:
            print(f"No records found for the range {date1} to {date2}.")
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
threading.Thread(target=log_data).start()
threading.Thread(target=radio).start()
app.run(host='0.0.0.0', port=80,debug=DEBUG)
