import json
import numpy as np
# Data to be written
dictionary = {}

inside_dictionary = {"weights":[], "bias": []}

device_num = 3

devices = []

for i in range(device_num):
    deviceName = "Device_"+str(i+1)
    devices.append(deviceName)
    dictionary[deviceName] = inside_dictionary

dictionary["global_weights"] = []
dictionary["global_bias"] = []

initial_weights = np.random.randn(3,3).tolist()
initial_bias = np.random.randn(1,3).tolist()

dictionary["global_weights"] = initial_weights
dictionary["global_bias"] = initial_bias
iman_break = 1
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
     outfile.write(json_object)


# read from json file

with open("sample.json", "r") as myfile:
    fileContent = json.load(myfile)
    weights = fileContent["global_weights"]
    bias = fileContent["global_bias"]
    print("weights are: ", weights)
    print("bias mat is: ", bias)
myfile.close()
new_weights = np.random.randn(3,3).tolist()
new_bias = np.random.randn(1,3).tolist()
fileContent["global_weights"] = new_weights
fileContent["global_bias"] = new_bias
jsonString = json.dumps(fileContent)
jsonFile = open("sample.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

# writing for each device

DeviceName = "Device_1"

with open("sample.json", "r") as myfile:
    fileContent = json.load(myfile)
    Device_1_weights = fileContent[DeviceName]["weights"]
    Device_1_bias = fileContent[DeviceName]["bias"]
    print("Device_1: weights are: ", Device_1_weights)
    print("Device_1: bias mat is: ", Device_1_weights)

myfile.close()

new_weights = np.random.randn(3,3).tolist()
new_bias = np.random.randn(1,3).tolist()
fileContent[DeviceName]["weights"] = new_weights
fileContent[DeviceName]["bias"] = new_bias
jsonString = json.dumps(fileContent)
jsonFile = open("sample.json", "w")
jsonFile.write(jsonString)
jsonFile.close()