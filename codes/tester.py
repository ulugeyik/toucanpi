from datetime import datetime #to know the correct date and write to file
from time import sleep #we all need some rest
from sense_hat import SenseHat  #this is what we use to sense
import csv # this one is for saving to files in csv
hat=SenseHat()
outdata=(3,datetime.now())
#get the time
outdata = (outdata,datetime.now())
#Gets the current orientation in radians, aircraft pitch, roll and yaw.
orient = hat.get_orientation_radians()
outdata= (datetime.now(), round(orient["pitch"],4),round(orient["roll"],4),round(orient["yaw"],4))
#print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))

#Gets the raw x, y and z axis magnetometer data.
magnet = hat.get_compass_raw()
outdata= (outdata, round(magnet["x"],4),round(magnet["y"],4),round(magnet["z"],4))
#print("x: {x}, y: {y}, z: {z}".format(**raw))
