from gpiozero import Button, MotionSensor
from picamera2 import Picamera2
from libcamera import Transform  # 1. Added for correct transform type
from signal import pause
from time import sleep
import os

# Component Configuration
button = Button(2)
pir = MotionSensor(4)

# Picamera2 Initialization & Setup
pic = Picamera2()
config = pic.create_preview_configuration(main={"size": (1280, 720)})

# 2. Fixed: Use Transform object instead of a string
config["transform"] = Transform(180) 

pic.configure(config)

# Start Camera Preview
pic.start()
print("Camera preview started. System is ready.")

# Variable for image indexing
i = 0

def stop_camera():
    print("\nStopping camera and exiting...")
    pic.stop()
    os._exit(0) 

def take_photo():
    global i
    i = i + 1
    save_path = f'/home/iot-team5/Desktop/image_{i}.jpg'
    
    print(f'Motion Detected! Capturing: image_{i}.jpg')
    pic.capture_file(save_path)
    
    print('Capture complete. Waiting for 10 seconds...')
    sleep(10)

# Connect Events
button.when_pressed = stop_camera
pir.when_motion = take_photo

try:
    pause()
except KeyboardInterrupt:
    pic.stop()
