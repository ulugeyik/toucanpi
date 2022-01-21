# Our first program 21/01/2022
# The goal of this programe is to record 2 sensor values every 2 seconds
# and save them to a file with time.

# This is to find we are on the computer.
from pathlib import Path
base_folder = Path(__file__).parent.resolve() #we save everything here
import csv # this one is for saving to files
from sense_hat import SenseHat  #this is what we use to sense
from datetime import datetime #this is to get the current time
from time import sleep #we all like to sleep :) to give a pause
from numpy import square, sqrt #to square number and to find squareroot

#ToucanPi sensor object 
tsense = SenseHat()

#Give the name of our date file
data_file = base_folder/'data20220121.csv'

#open the file
with open(data_file, 'w', buffering=1) as f:
    writer = csv.writer(f)
    header = ("Date/time", "Temperature", "AccelerationTotal")
    writer.writerow(header)
    for i in range(30):
        acc= sqrt(square(tsense.accelerometer_raw["x"])+square(tsense.accelerometer_raw["y"])+square(tsense.accelerometer_raw["z"]))
        row = (datetime.now(), tsense.temperature, acc)
        writer.writerow(row)
        sleep(2)

print("end")
#for next week
# reduce decimal places, round
# explain filename structure
# learn how to plot
