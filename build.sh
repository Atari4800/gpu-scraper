apt-get update && apt-get upgrade -y
apt-get install python3-pip -y
apt-get install python3-tk -y
apt-get install python3-bs4 -y
apt-get install python3-pytest -y
apt install xdg-utils -y
pip3 install selenium -y
pip3 install python-crontab -y
xdg-settings get default-web-browser > defaultBrowser.txt 
chmod -x test_productListNoWrite.json
chmod +x ./drivers/*
echo "build complete"
