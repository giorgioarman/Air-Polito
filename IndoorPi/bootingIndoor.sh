#/bin/sh

echo "Hello! I was executed on boot correctly!" > /tmp/bootingIndoor.txt

python3 /home/pi/Desktop/Project/bridgeWS.py &
python3 /home/pi/Desktop/Project/ipqaCalculation.py &
python3 /home/pi/Desktop/Project/sendToOnlineDB.py &

echo "I executed every python script!" >> /tmp/bootingIndoor.txt
