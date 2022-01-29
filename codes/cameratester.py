from picamera import PiCamera #to use the camera
cam = PiCamera()
#cam.resolution = (1296,972) #TODO: adjust to the HQ camera resolution
# TODO: find out why I Can not use this resolution
cam.resolution = (4056,3040) #highest resolution, this is the one from example on flickr
cam.capture("test.jpg")