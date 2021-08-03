apt-get update && apt-get upgrade 
apt-get install python3-pip 
apt-get install python3-tk 
apt-get install python3-bs4 
apt-get install python3-pytest 
apt install xdg-utils 
pip3 install selenium 
pip3 install python-crontab 
xdg-settings get default-web-browser > defaultBrowser.txt 
chmod -wx test_productListNoWrite.json
chmod +x ./drivers/*
echo "build complete"
