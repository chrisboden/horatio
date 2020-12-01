import serial
import time

ser = serial.Serial('COM6', 115200, timeout = 1)  # open serial port
time.sleep(2)    
print(ser.readline())

gcodes = []
gcodes.append('G90')
gcodes.append('G28')

square = 'square'
triangle = 'triangle'
circle = 'circle'
groundLvl = '-391'

def move(x, y, z):
    if x == '':
        isX = ''
    else:
        isX = ' X'
    if y == '':
        isY = ''
    else:
        isY = ' Y'
    if z == '':
        isZ = ''
    else:
        isZ = ' Z'
    gcodes.append('G01'+ isX + str(x) + isY + str(y) + isZ + str(z))

def draw(shape, centerX, centerY, size):
    if size < 1:
        print('error: size must not be smaller than 1')

    elif shape == 'square':
        valX1 = str(centerX + size/2)
        valX2 = str(centerX - size/2)
        valY1 = str(centerY + size/2)
        valY2 = str(centerY - size/2)
        #move to start pos
        gcodes.append('G01 X'+valX1+' Y'+valY1+' Z-350')
        #pen down
        gcodes.append('G01 Z'+groundLvl)
        #draw 4 sides
        gcodes.append('G01 X'+valX1+' Y'+valY2)
        gcodes.append('G01 X'+valX2+' Y'+valY2)
        gcodes.append('G01 X'+valX2+' Y'+valY1)
        gcodes.append('G01 X'+valX1+' Y'+valY1)
        #pen up
        gcodes.append('G01 Z-350')
        #center
        gcodes.append('G01 X0 Y0')

    elif shape == 'triangle':
        valX1 = str(centerX + size/2)
        valX2 = str(centerX - size/2)
        valY1 = str(centerY + size/2)
        valY2 = str(centerY - size/2)
        
        #move to bottom left
        gcodes.append('G01 X'+valX2+' Y'+valY2)
        # pen down
        gcodes.append('G01 Z'+groundLvl)
        # move to top
        gcodes.append('G01 X'+str(centerX)+' Y'+valY1)
        # move to bottom right
        gcodes.append('G01 X'+valX1+' Y'+valY2)
        # move to bottom left
        gcodes.append('G01 X'+valX2+' Y'+valY2)
        # pen up
        gcodes.append('G01 Z-350')
        # center
        gcodes.append('G01 X0 Y0')

    elif shape == 'circle':
        halfSize = str(size/2)
        valY1 = str(centerY + size/2)
        valY2 = str(centerY - size/2)

        # move to top
        gcodes.append('G01 X'+str(centerX)+' Y'+valY1)
        # pen down
        gcodes.append('G01 Z'+groundLvl)
        # arc to bottom
        gcodes.append('G02 I0 J-'+halfSize+'X'+str(centerX)+' Y'+valY2)
        # arc to top
        gcodes.append('G02 I0 J'+halfSize+'X'+str(centerX)+' Y'+valY1)
        # pen up
        gcodes.append('G01 Z-350')
        # center
        gcodes.append('G01 X0 Y0')

    else:
        print('error: invalid shape')

def start():
    for gcode in gcodes:
            print(gcode)
            ser.write(str.encode((gcode + '\n')))

########################
draw(square, 0, 0, 80)
start()
########################

ser.close()             # close port