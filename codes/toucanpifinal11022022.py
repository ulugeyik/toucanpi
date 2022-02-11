"""
ToucanPi Team 
Members: Gaia, Iris, Tom
Mentor: Turgut Durduran
Location: Castelldefels, Spain

Description of the code:

This code consists of recording data from these sensors:
Orientation, magnetometer, gyroscope and accelerometer.
We use many libraries including:
orbit, picamera, pathlib, datetime, time, sense_hat, csv, threading and logzero.

We used daemon threads to make sure our program finishes on time.
We used a few functions to read our sensors and to store the data.
We will take pictures every 25 seconds to calculate the velocity of the ISS.
Our main goal is to prove that the gravity is not actually 0 in space, even though everything is always floating.

"""

##############################################
#Let's load our libraries
##############################################

from orbit import ISS #to find where ISS is.
from picamera import PiCamera #to use the camera
from pathlib import Path #to find where our files are
from datetime import datetime #to know the correct date and write to file
from time import sleep #we all need some rest
from sense_hat import SenseHat  #this is what we use to sense
import csv # this one is for saving to files in csv
from threading import Thread #to run the code for a set time
from logzero import logger, logfile #suggested by AstroPi Guide

##############################################

##############################################
#Define our functions
##############################################

def convert(angle):
    """   
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    
    This is from Astropi documentation.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data.
       Note: "three timestamp tags: IFD0.DateTime,
       EXIF.DateTimeOriginal, and EXIF.DateTimeDigitized" are added by
       default.  YYYY:MM:DD HH:MM:SS 
       Info from:
       https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.exif_tags
      This is from Astropi documentation
      To capture a frame from the camera and add exif info with ISS location
    """
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

#This is what we want to sense from the sensehat
def sensedata(hat,counter):
    """Get and organize the sensor data from sensehat.
       Based on https://pythonhosted.org/sense-hat/api/#environmental-sensors
       Input: hat , sensehat info, counter current number of data
      Output: Formatted string for output to csv file
    """
    #NOTE: Can we do a more elegant solution with f-strings?

    #Gets the current orientation in radians, aircraft pitch, roll and yaw.
    orient = hat.get_orientation_radians()

    #Gets the raw x, y and z axis magnetometer data.
    magnet = hat.get_compass_raw()
    
    #Gets the raw x, y and z axis gyroscope data.
    #NOTE: Not sure this versus orientation ?
    gyro = hat.get_gyroscope_raw()
 
    #Gets the raw x, y and z axis accelerometer data.
    acc = hat.get_accelerometer_raw()
 
    #Add the ISS position, for redundancy
    location = ISS.coordinates()
    #TODO: Check if I should add E, W etc.

    #TODO: can we know the altitude of ISS?
    outdata = (
        counter,
        datetime.now(),
        round(orient["pitch"],4),
        round(orient["roll"],4),
        round(orient["yaw"],4),
        round(magnet["x"],4),
        round(magnet["y"],4),
        round(magnet["z"],4),
        round(gyro["x"],4),
        round(gyro["y"],4),
        round(gyro["z"],4),
        round(acc["x"],4),
        round(acc["y"],4),
        round(acc["z"],4),
        round(location.latitude.degrees,4),
        round(location.longitude.degrees,4),
    )

    return outdata

 
def maintask():
    """
    This function is used to open our datafile during the program and record our data.
    """
    with open(data_file, 'w', buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        counter=1 #create a counter to know what we did
        while True:
            row = sensedata(toucanhat,counter)
            writer.writerow(row) #TODO: We may need to flush after this, check time
            if not counter%5: #too many photos, let's do this every 5th data entry
               pic_filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
               pic_path = f"{base_folder}/toucanphoto_{pic_filename}"
               capture(cam,pic_path)
               logger.info(f"Count {counter} file {pic_filename}")
            else :
               logger.info(f"Count {counter}") 
            counter+=1 #increase counter
            sleep(5) #TODO: Fix duration, it takes 1 second extra approx

    
##############################################



##############################################
#Preparatory actions

#TODO: consider a simpler name
toucanhat=SenseHat()

#AstroPi requires that files are all saved on the same folder as the code
#Get this information
base_folder = Path(__file__).parent.resolve()

#This is the header to be used for the csv file
header = ("Counter", "Date/Time", "OrientPitch", "OrientRoll", "OrientYaw", "MagnetX", "MagnetY", "MagnetZ", "GyroX", "GyroY", "GyroZ", "AccX", "AccY", "AccZ", "Lat", "Long")

#Give the name of our data file
data_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
data_file = f"{base_folder}/toucandata_{data_filename}.csv"

# Set a logfile name
logfile(f"{base_folder}/toucanevents_{data_filename}.log")

#Initialize sensors and camera

#start with the camera
cam = PiCamera()
cam.resolution = (4056,3040) #highest resolution, this is the one from example on flickr

#We are following a suggestion to use daemon threads to execute code
t= Thread(target=maintask)
t.daemon = True

##############################################
#The following is a way to catch errors.
try:
    logger.info("Start") # Log event
    t.start() #run the main task
#    sleep(10700) #sleep <10800, 3 hours seconds and everything should finish
    sleep(180)
except KeyboardInterrupt:
    logger.info("Quit") # Log event
except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')