apt-get update && apt-get upgrade -y
apt-get install python3-pip
apt-get install tkinter
apt-get install python3-bs4

pip3 install selenium
pip3 install python-crontab
xdg-settings get default-web-browser > defaultBrowser.txt 
echo "build complete"
