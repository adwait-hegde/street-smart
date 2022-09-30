import cv2
import numpy as np
from vehicle_detector import VehicleDetector
from EmergencyVehicleDetection.emergencyVehicle import EmergencyVehicleDetection
import time

class VehicleDensityCalculator:
	def __init__(self,):
		self.vehicleDetector = VehicleDetector()
		self.vehicleClass = {
			2: 4,
			3: 2,
			5: 6,
			6: 0,
			7: 6,
		}
		self.laneCount = 2
		self.frameOffset = 60
		self.frameCounter = 0
		self.curr_vDensity = 0
		self.isEmergencyVehiclethere = 0
		self.emergencyVehicleDetector = EmergencyVehicleDetection()

	def frameEnhancer(self, imgFrame):
		gray = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2GRAY)
		imgFrame = np.zeros_like(imgFrame)
		imgFrame[:,:,0] = gray
		imgFrame[:,:,1] = gray
		imgFrame[:,:,2] = gray
		return imgFrame

	def calculate(self, imgFrame, feedNo, lr):
		wheelCount = 0
		imgFrameGray = self.frameEnhancer(imgFrame)
		vehicleCount, classLst = self.vehicleDetector.detect_vehicles(imgFrameGray)
		for box, vehicleCat in zip(vehicleCount, classLst):
			x, y, w, h = box
			imgFrame = cv2.rectangle(imgFrame, (x, y), (x+w, y+h), (217, 22, 22), 3)
			if lr[0] != 0 and lr[1] != 0:
				cv2.imshow(f"CCTV {feedNo}", imgFrame[:, lr[0]:lr[1]])
			elif lr[0] != 0 and lr[1] == 0:
				cv2.imshow(f"CCTV {feedNo}", imgFrame[:, lr[0]:])
			elif lr[0] == 0 and lr[1] != 0:
				cv2.imshow(f"CCTV {feedNo}", imgFrame[:, :lr[1]])
			elif lr[0] == 0 and lr[1] == 0:
				cv2.imshow(f"CCTV {feedNo}", imgFrame[:, :])
			wheelCount += self.vehicleClass[vehicleCat]
		print(f"for feed {feedNo}, wheelcount: {wheelCount}")
		return imgFrame, wheelCount/self.laneCount

	def vDensity(self, feedNo, lr):
		feed = cv2.VideoCapture(f'./Training Testing Videos/Feed {feedNo}.mp4')
		while True:
			success, img = feed.read()
			imgResized = cv2.resize(img, (0, 0), None, 0.5, 0.5)
			self.isEmergencyVehiclethere = self.emergencyVehicleDetector.call(success, imgResized)
			if self.isEmergencyVehiclethere:
				print("Emergency Vehicle Detected!!!")
			img, self.curr_vDensity = self.calculate(imgResized, feedNo, lr)
			cv2.imshow(f"CCTV {feedNo}", imgResized)
			if cv2.waitKey(1) & 0xFF == ord('1'):
				break
			self.frameCounter += 1
		feed.release()
		cv2.destroyAllWindows()
