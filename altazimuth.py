# altazimuth calculations for pikontroll
# based on c code from http://pikon.patrickaalto.com/pikonblog.html
# jes 2018

import math
import time

# return current unix time in microseconds
def GetNow():
    return time.time() * 1000000

# https://answers.yahoo.com/question/index?qid=20080630193348AAh4zNZ
# return current "local sidereal degrees"
def CalculateLocalSiderealDegrees(longitude, utcNow):
    D = (utcNow - 946728000 * 1000000) / (1000000.0*60.0*60.0*24.0)
    return math.fmod(280.461+360.98564737 * D + longitude, 360.0)

# return (azimuthDegrees, altitudeDegrees)
# http://star-www.st-and.ac.uk/~fv/webnotes/chapter7.htm
# http://www.stargazing.net/kepler/altaz.html
def ComputeAltAzimuth(utcNow, longitudeDegrees, latitudeDegrees, rightAscensionHours, declinationDegrees):
    localSiderealDegrees = CalculateLocalSiderealDegrees(longitudeDegrees, utcNow)
    rightAscensionDegrees = rightAscensionHours * 15.0;  # Convert hours to degrees by multiplying with 15
    hourAngleDegrees = localSiderealDegrees - rightAscensionDegrees
    if hourAngleDegrees < 0.0:
        hourAngleDegrees += 360.0
    hourAngleRadians = 2.0 * math.pi / 360.0 * hourAngleDegrees
    declinationRadians = 2.0 * math.pi / 360.0 * declinationDegrees
    latitudeRadians = 2.0 * math.pi / 360.0 * latitudeDegrees

    altitudeRadians = math.asin(math.sin(declinationRadians) * math.sin(latitudeRadians) + math.cos(declinationRadians) * math.cos(latitudeRadians) * math.cos(hourAngleRadians))

    azimuthRadians = math.acos((math.sin(declinationRadians) - math.sin(altitudeRadians) * math.sin(latitudeRadians)) / (math.cos(altitudeRadians) * math.cos(latitudeRadians)))

    altitudeDegrees = 360.0 / (2 * math.pi) * altitudeRadians
    azimuthDegrees = 360.0 / (2 * math.pi) * azimuthRadians

    if math.sin(hourAngleRadians) > 0:
        azimuthDegrees = 360.0 - azimuthDegrees

    return (azimuthDegrees, altitudeDegrees)

# return (rightAscensionHours, declinationDegrees)
def ComputeRaDec(utcNow, longitudeDegrees, latitudeDegrees, azimuthDegrees, altitudeDegrees):
    localSiderealDegrees = CalculateLocalSiderealDegrees(longitudeDegrees, utcNow)
    latitudeRadians = 2.0 * math.pi / 360.0 * latitudeDegrees
    altitudeRadians = 2.0 * math.pi / 360.0 * altitudeDegrees
    azimuthRadians = 2.0 * math.pi / 360.0 * azimuthDegrees

    declinationRadians = math.asin(math.sin(latitudeRadians) * math.sin(altitudeRadians) + math.cos(latitudeRadians) * math.cos(altitudeRadians) * math.cos(azimuthRadians))

    # calculate the hour-angle using both cosine rule and sine rule, so that we can disambiguate
    # (both arcsine and arccosine are ambiguous: cosine is mirrored about 180 degrees, sine is mirrored
    # in two sections, about 90 degrees and 270 degrees)
    hourAngleRadiansCosineRule = math.acos((math.sin(altitudeRadians) - math.sin(declinationRadians) * math.sin(latitudeRadians))/(math.cos(declinationRadians) * math.cos(latitudeRadians)))
    hourAngleRadiansSineRule = math.asin((-math.sin(azimuthRadians) * math.cos(altitudeRadians)) / math.cos(declinationRadians))
    hourAngleRadians = hourAngleRadiansCosineRule
    if hourAngleRadiansSineRule < 0:
        hourAngleRadians = 2.0 * math.pi - hourAngleRadiansCosineRule

    hourAngleDegrees = 360.0 / (2.0 * math.pi) * hourAngleRadians
    rightAscensionDegrees = localSiderealDegrees - hourAngleDegrees
    if rightAscensionDegrees < 0.0:
        rightAscensionDegrees += 360.0
    rightAscensionHours = rightAscensionDegrees / 15.0
    declinationDegrees = 360.0 / (2.0 * math.pi) * declinationRadians
    return (rightAscensionHours, declinationDegrees)
