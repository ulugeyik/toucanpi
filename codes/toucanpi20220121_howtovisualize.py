#2022/01/21 Added by Turgut for next time to see how to visualize
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

mydata = pd.read_csv('../data/data20220121.csv', parse_dates={ 'newdate': ['Date/time'] })



plt.figure()
plt.plot(mydata.newdate,mydata.Temperature)
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.show()

plt.figure()
plt.plot(mydata.newdate,mydata.AccelerationTotal)
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.show()


from myorbit import ISS #this is for non-astropi computers
#from orbit import ISS #this is for astropi computers
from skyfield.api import load, wgs84

#wgs84 info https://rhodesmill.org/skyfield/api-topos.html
ts = load.timescale() #for simplicity

#probably I am not doing this well, but assume that this is needed
from pytz import timezone
timezone = timezone("UTC")
# from https://www.kite.com/python/answers/how-to-apply-a-function-to-a-list-in-python
t = map(timezone.localize,mydata.newdate) #now all have a timezone
t = ts.from_datetimes(t)
position = ISS.at(t)

# does not work on Astropi since it has an old library
#lat, lon = wgs84.latlon_of(position) #astropi has an old version of library
#mydata["lat"]=lat.degrees
#mydata["lon"]=lon.degrees

#on astropi use me
loc = position.subpoint()
mydata["lat"]= loc.latitude.degrees
mydata["lon"]= loc.longitude.degrees



import plotly.express as px
fig = px.scatter_geo(mydata,lat=mydata.lat,lon=mydata.lon)
fig.update_layout(title = 'World map', title_x=0.5)
fig.show()
