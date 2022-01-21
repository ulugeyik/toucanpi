import gpiozero

class MotionSensor(gpiozero.MotionSensor):
    """
    The MotionSensor class simplifies access to the Astro Pi
    motion sensor by abstracting away the fact that it is
    connected to GPIO pin 12.
    
    Other than that, the class is directly derives from
    gpiozero's MotionSensor Class and inherits its interface:
    gpiozero.readthedocs.io/en/stable/api_input.html#motionsensor-d-sun-pir
    """
    
    def __init__(self, **kwargs):
        super().__init__(pin=12, **kwargs)