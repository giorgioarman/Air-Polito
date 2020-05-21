#/bin/sh

echo "Hello! I was executed on boot correctly!" > /tmp/bootingIndoor.txt

python /home/pi/Desktop/Project/DHT_Sensor.py &
python /home/pi/Desktop/Project/Data_Acquisition.py &
python /home/pi/Desktop/Project/sendData.py &

echo "I executed every python script!" >> /tmp/bootingIndoor.txt
