import os,datetime
from flask import Flask,render_template

DEBUG=False

app=Flask("website")

@app.route("/")
def main():
    
    return render_template("index.html")

@app.route('/get-live-data')
def get_live_data():
    temp=int(open("temp.txt",'r').read())
    heure=datetime.datetime.now()
    h=heure.hour
    m=heure.minute
    s=heure.second
    return f"""
<p>Température : {temp}°C<br><br>
Time : {h} : {m} : {s}
</p>
    """

app.run(host='0.0.0.0', port=80,debug=DEBUG)