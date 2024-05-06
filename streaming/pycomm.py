import serial
from ML.ML_ModelL import classifications

for i in classifications[0:3]:
    #get number for predictions
    pred = i[[i==1.0]]
    print(pred)

# # Open the serial port
# ser = serial.Serial('COM3', 9600)

# # Send a single digit integer to Arduino
# #num = int(input("Enter number: "))
# ser.write(str(num).encode())

# # Close the serial port
# ser.close()
