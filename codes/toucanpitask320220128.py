#Task 3 ToucanPi 2022/02/04
#Goal: Near complete task including timing & data sizing


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

#to make our life simpler with a shorter name
toucanhat=SenseHat()
##############################################

##############################################
#Define our functions
##############################################

#This is from Astropi documentation
def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

#This is from Astropi documentation
#To capture a frame from the camera and add exif info with ISS location
def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data.
       Note: "three timestamp tags: IFD0.DateTime,
       EXIF.DateTimeOriginal, and EXIF.DateTimeDigitized" are added by
       default.  YYYY:MM:DD HH:MM:SS 
       Info from:
       https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.exif_tags
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
def sensedata(hat):
    """Get and organize the sensor data from sensehat.
       Based on https://pythonhosted.org/sense-hat/api/#environmental-sensors
       Input: hat , sensehat info
      Output: Formatted string for output to csv file
    """
    #NOTE: Can we do a more elegant solution with f-strings?
    
    #get the time
    outdata = datetime.now()
    #Gets the current orientation in radians, aircraft pitch, roll and yaw.
    orient = hat.get_orientation_radians()
    outdata= outdata + (orient["pitch"],orient["roll"],orient["yaw"])
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))

    #Gets the raw x, y and z axis magnetometer data.
    magnet = hat.get_compass_raw()
    outdata= outdata + (magnet["x"],magnet["y"],magnet["z"])
    #print("x: {x}, y: {y}, z: {z}".format(**raw))
    
    #Gets the raw x, y and z axis gyroscope data.
    #NOTE: Not sure this versus orientation ?
    gyro = hat.get_gyroscope_raw()
    outdata= outdata + (gyro["x"],gyro["y"],gyro["z"])
    #print("x: {x}, y: {y}, z: {z}".format(**raw))

    #Gets the raw x, y and z axis accelerometer data.
    acc = hat.get_accelerometer_raw()
    outdata= outdata + (acc["x"],acc["y"],acc["z"])
    #print("x: {x}, y: {y}, z: {z}".format(**raw))

    #Add the ISS position, for redundancy
    point = ISS.coordinates()
    outdata= outdata + (point.latitude, point.longitude)
    #TODO: Check if I should add E, W etc.

    return outdata

    
##############################################



##############################################
#Preparatory actions

#AstroPi requires that files are all saved on the same folder as the code
#Get this information
base_folder = Path(__file__).parent.resolve()

#This is the header to be used for the csv file
header = ("Date/Time", "OrientPitch", "OrientRoll", "OrientYaw", "MagnetX", "MagnetY", "MagnetZ", "GyroX", "GyroY", "GyroZ", "AccX", "AccY", "AccZ", "Lat", "Long")

#Give the name of our data file
data_filename = datetime.now().strftime("%Y%m%d_%H%M%S.csv")
data_file = f"{base_folder}/toucandata_{data_filename}"


#Initialize sensors and camera

#start with the camera
cam = PiCamera()
cam.resolution = (1296,972) #TODO: adjust to the HQ camera resolution
#cam.resolution = (4050,3040) #highest resolution

#TODO: Is this necessary?
#IMU sensor
#Enable compass, gyroscope, accelerometer
toucanhat.set_imu_config(True, True, True)  



##############################################

#The following is a way to catch errors.
try:
    print('Start')
    #To show us that program is ready
    toucanhat.show_message("Show time!")

   
    #open the file
    with open(data_file, 'w', buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        while True:
            hat.clear([120, 0, 100])
            pic_filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
            pic_path = f"{base_folder}/toucanphoto_{pic_filename}"
            capture(cam,pic_path)
            print("Recorded %s" % pic_filename)
            row = sensedata(toucanhat)
            writer.writerow(row)
            sleep(2.5)
            hat.clear([0, 0, 0])
            sleep(2.5)
except KeyboardInterrupt:
    print('Quit')
