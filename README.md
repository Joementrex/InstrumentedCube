
# A low cost instrumented cube for assessing robotic performance from a first person perspective 

This repository contains the content documenting the files for the instrumented cube

The data collected has been ommitted from this repository as it exceeds the github 100MB limit.



## 3D Files

The 3D files folder contains the STL files of the instrumented object.



## Code 

The code folder contains all the code developed during development including the programming for the microcontrollers and local data collection, training and inference. 

The final code used for demonstration was the manualFinal python file and manualCollection Final running in python and the microcontrollers used ESP32C3_Master_sensors2 and ESP32_Slave_sensors.

The libraries in the data collection and training folder contain custom tools for commanding a 3D printer over the network that is connected with octoprint and contains functions that will estimate the duration of the movement of the printer to prevent sending many gcode commands and executing code before finishing movement. 
A library called ESPReader was also developed that reads and parses the incoming Serial data from the device.

The remaining code uploaded was just for development purposes for the visualisation, training and inference. Some versions of the code contain methods for saving version history of the data collected to prevent training when there is no new training data and skip to inference. 


## PCB 

The custom PCB for the sensors were developed by another student and used in this project and is included in the PCB folder
## Assembly

To assemble the device, 3D print the 3D model files with the inner shell and lid printed in a tough material such as PETG to ensure longevitiy and durability for extended use of the device under high forces, and print the bottom face to enclose the bottom.
Do the same for the reciever print model and assemble it. The antenna can be removed on the reciever without limiting range greatly.

The modules and the outer shell is printed out of TPU material, TPU 95A was used but printers capable of printing a softer material can be used for better performance. 

Once printed get the PCB's made and assemble them with the appropriate resistor and sensor.
Wire up the sensors in groups of 3 with optional JST connectors for simple disassembly and glue them into the inserts in the modules. To provide face swaps and easy assembly and disassembly wire up the order of the sensors in each face the same order.

Glue 5 magnets around the inner shell, and feed the wires of the modules through the holes in the inner shell. Heat insert m2 inserts into the hole for the lid screw in the inner shell and 4 more inside the lid for the IO expander and screw the IO expander onto the lid. 

Place the ESP32C3 microcontroller in the designated slot in the inner shell and place the battery inside the shell. Connect the IO expander to the microcontroller and the modules to the IO expander. Screw on the bottom lid.

Face the top module with the peak sensor facing the forward direction and the remaining modules have the peak sensor facing upwards. Enclose the modules with the outer shell and place the bottom face onto the device to secure the cube together and provide a flat surface. 

Upload the code to the ESP32C3 reciever and transmitter. 


## Code Execution 

To run the code, the main working example is the DataCollectionManualFinal that will prompt the user to press on each of the 4 contact points on the face and collect a range of sample data from the device. Once data has been collected manualFinal training will train the data on a random forest regressor and run inference on the file with a simple 2D visualiser showing contacts, forces and varying colour for each face.

The reposatory also contains many examples of using different training methods, different data collections and many different visualisers ranging from automatic to manual data collection. What combination of tools used is up to the researcher. 