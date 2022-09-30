import requests

url = 'http://127.0.0.1:5000/traffic'
data = {
    'density1': v1.curr_vDensity,
    'density2': v2.curr_vDensity,
    'density3': v3.curr_vDensity,
    'density4': v4.curr_vDensity,
    'emv1': v1.isEmergencyVehiclethere,
    'emv2': v2.isEmergencyVehiclethere,
    'emv3': v3.isEmergencyVehiclethere,
    'emv4': v4.isEmergencyVehiclethere,
 }

x = requests.post(url, data=data)

print(x.json)