"orbit: Modules for interfacing with the Astro Pi"

__project__ = 'orbito'
__version__ = '1.1.0'
__requires__ = ['gpiozero', 'skyfield']
__entry_points__ = {}
__scripts__ = []

from .motion_sensor import MotionSensor
from .telemetry import ISS