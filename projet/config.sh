# Update your package list
sudo apt-get update

# Install dependencies for building the library
sudo apt-get install python3-dev python3-setuptools libboost-python-dev python3-pip

# Install the RF24 library via pip
sudo pip install pyrf24 flask netifaces --break-system-packages