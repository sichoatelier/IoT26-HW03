from gpiozero import Button, MotionSensor
from picamera2 import Picamera2
from signal import pause
from time import sleep
import os

# 1. Component Configuration
# Button is connected to GPIO 2, PIR sensor to GPIO 4
button = Button(2)
pir = MotionSensor(4)

# 2. Picamera2 Initialization & Setup
pic = Picamera2()
config = pic.create_preview_configuration(main={"size": (1280, 720)})

# Set rotation for v1.3 camera
config["transform"] = "rotate180" 
pic.configure(config)

# 3. Start Camera Preview
pic.start()
print("Camera preview started.")

# Variable for image indexing
i = 0

# Stop the camera and exit the program when the button is pressed
def stop_camera():
    print("\nStopping camera and exiting...")
    pic.stop()
    os._exit(0) 

# Take a photo when motion is detected
def take_photo():
    global i
    i = i + 1
    
    # Path settings - make sure 'iot-team5' matches your username
    save_path = f'/home/iot-team5/Desktop/image_{i}.jpg'
    
    print(f'Motion Detected! Capturing: image_{i}.jpg')
    pic.capture_file(save_path)
    
    print('Capture complete. Waiting for 10 seconds...')
    sleep(10)

# Connect Events
button.when_pressed = stop_camera
pir.when_motion = take_photo

try:
    print("System is Ready. Press the button to exit.")
    pause()
except KeyboardInterrupt:
    pic.stop()
