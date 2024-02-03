import serial

# Open the serial port
ser = serial.Serial('COM3', 9600)

# Send a single digit integer to Arduino
num = int(input("Enter number: "))
ser.write(str(num).encode())

# Close the serial port
ser.close()
