from orbit import ISS #to find where ISS is.

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


point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
south, exif_latitude = convert(point.latitude)
west, exif_longitude = convert(point.longitude)
point.latitude.degrees
point.longitude.degrees