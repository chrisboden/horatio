import serial
import time

ser = serial.Serial('COM6', 115200, timeout = 1)  # open serial port
time.sleep(2)    
print(ser.readline())

positions = [[-55, -30], [44, -107], [152, -36], [50, 87], [-65, 93], [-126, -64]]

gcodes = []
gcodes.append('G90')
gcodes.append('G28')

for i in range(len(positions)):
    gcodes.append('G01 Z-350')
    gcodes.append('G01 X'+str(positions[i][0])+' Y'+str(positions[i][1]))
    gcodes.append('G01 Z-385')
    gcodes.append('G4 P1000')
    gcodes.append('G01 Z-350')
    gcodes.append('G01 X0 Y0')

for gcode in gcodes:
        ser.write(str.encode((gcode + '\n')))