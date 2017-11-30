if [ "$EUID" -ne 0 ]
    then echo "Permission denied. Please run as root"
    exit
fi

apt install python3
apt-get install mongodb python3-pip
pip3 install requests bs4 lxml tabulate pytz
pip3 install -Iv pymongo==2.9
