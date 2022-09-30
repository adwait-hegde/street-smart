import time
import cv2
from detector import VehicleDensityCalculator
import threading
import requests

v1, v2, v3, v4 = VehicleDensityCalculator(), VehicleDensityCalculator(), VehicleDensityCalculator(), VehicleDensityCalculator()

url = 'http://127.0.0.1:5000/traffic'

thread1 = threading.Thread(target=v1.vDensity, args=[1, (100, 0)])
thread2 = threading.Thread(target=v2.vDensity, args=[2, (0, 0)])
thread3 = threading.Thread(target=v3.vDensity, args=[6, (0, 0)])
thread4 = threading.Thread(target=v4.vDensity, args=[2, (0, 0)])

thread1.start()
thread2.start()
thread3.start()
thread4.start()

data = dict()

cur_lane = 0
resp_time = None 
cur_time = 45


while True:
	data = {
		'density1': v1.curr_vDensity,
		'density2': v2.curr_vDensity,
		'density3': v3.curr_vDensity,
		'density4': v4.curr_vDensity,
		'emv1': v1.isEmergencyVehiclethere,
		'emv2': v2.isEmergencyVehiclethere,
		'emv3': v3.isEmergencyVehiclethere,
		'emv4': v4.isEmergencyVehiclethere,
		'cur_lane': cur_lane,
		'resp_time': resp_time,
		'cur_time': cur_time,
 	}

	responseRecvd = requests.post(url, data=data).json()


	cur_lane = responseRecvd['cur_lane']
	resp_time = responseRecvd['resp_time']
	cur_time = responseRecvd['cur_time']

	time.sleep(2)