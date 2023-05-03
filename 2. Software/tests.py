import serial
import time

ser = serial.Serial('COM6', 9600)  # Replace 'COM3' with the correct port name for your Arduino
time.sleep(2)

while True:
    # Prompt the user for a command
    command = input("Enter command (A or B followed by a speed value): ")
    if command == "go":
        ser.write("R,220\nL,160\n".encode())  # Send both motor commands in the same block
    if command == "stop":
        ser.write("R,188\nL,188\n".encode())  # Send both motor commands in the same block
    if command == "run":
        ser.write("R,254\nL,122\n".encode())  # Send both motor commands in the same block
    if command == "ru":
        ser.write("R,122\nL,254\n".encode())  # Send both motor commands in the same block
    # Send the command over the serial connection
    ser.write(command.encode())
    time.sleep(0.1)  # Wait for the Arduino to process the command
    
    
    