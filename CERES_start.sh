mv /home/pi/CERES/runLog.log /home/pi/CERES/logs/runLog"_$(date '+%Y-%m-%d')".log
touch /home/pi/CERES/runLog.log
screen -S CERES -t CERES -L /home/pi/CERES/runLog.log -d -m /usr/local/bin/python3.6 /home/pi/CERES/py_src.sim/main.py
