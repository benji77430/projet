sudo apt-get update
sudo apt-get install python3-dev python3-setuptools libboost-python-dev python3-pip
sudo python --break-system-packages -r requirements.txt
sudo mv website.service /etc/systemd/system/website.service
sudo systemctl daemon-reload
sudo systemctl enable website.service
sudo systemctl start website.service