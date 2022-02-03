#Task 2 ToucanPi 2022/01/28
#Goal: Read sensors and camera info regular intervals and save
#https://projects.raspberrypi.org/en/projects/code-for-your-astro-pi-mission-space-lab-experiment/5
#Refer to the flowchart

#Let's load our libraries
from orbit import ISS #to find where ISS is.
from picamera import PiCamera #to use the camera
from pathlib import Path #to find where our files are
from datetime import datetime #to know the correct date and write to file
from time import sleep #we all need some rest
from sense_hat import SenseHat  #this is what we use to sense
import csv # this one is for saving to files in csv

#to make our life simpler
hat=SenseHat()


#Define our functions
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

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
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

#AstroPi requires that files are all saved on the same folder as the code
#Get this information
base_folder = Path(__file__).parent.resolve()
header = ("Date/time", "Temperature", "AccelerationZ")
#Give the name of our date file
data_filename = datetime.now().strftime("%Y%m%d_%H%M%S.csv")
data_file = f"{base_folder}/toucandata_{data_filename}"


#Set Initialize sensors and camera
cam = PiCamera()
cam.resolution = (1296,972) #adjust to the HQ camera resolution
#cam.resolution = (4050,3040) #highest resolution

#The following is a way to catch errors.
try:
    print('Start')
    #To show us that program is ready
    hat.show_message("Ready to roll!")

   
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
            row = (datetime.now(), hat.temperature, hat.accelerometer_raw["y"])
            writer.writerow(row)
            sleep(2.5)
            hat.clear([0, 0, 0])
            sleep(2.5)
except KeyboardInterrupt:
    print('Quit')
