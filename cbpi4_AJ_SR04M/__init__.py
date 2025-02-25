import os
import logging
import RPi.GPIO as GPIO
import asyncio
import time
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType
from cbpi.api.config import ConfigType

glogger = logging.getLogger(__name__)

@parameters([
    Property.Select(label="Ultrasonic Trig Pin", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="Trigger Pin"),
    Property.Select(label="Ultrasonic Echo Pin", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="Echo Pin"),
    Property.Number(label="Pot Diameter", configurable=True, description="Pot Diameter in cm"),
    Property.Number(label="Mounting Height", configurable=True, description="Mounting Height in cm"),
    Property.Select(label="Interval", options=[1, 2, 5, 10, 30, 60], description="Measurement Interval in Seconds")
])
class AJ_SR04M_volume(CBPiSensor):
    def __init__(self, cbpi, id, props):
        super(AJ_SR04M_volume, self).__init__(cbpi, id, props)
        self.value = 0
        self.interval = int(self.props.get("Interval", 2))
        self.trig_pin = int(self.props.get("Ultrasonic Trig Pin", 23))
        self.echo_pin = int(self.props.get("Ultrasonic Echo Pin", 24))
        self.pot_diameter = float(self.props.get("Pot Diameter", 40))
        self.mounting_height = float(self.props.get("Mounting Height", 50))
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    async def run(self):
        while self.running:
            distance = self.measure_distance()
            self.value = self.calculate_volume(distance)
            # self.log_data(self.value)
            self.push_update(self.value)
            await asyncio.sleep(self.interval)

    def measure_distance(self):
        try:
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            
            start_time, stop_time = None, None
            
            timeout = time.perf_counter() + 0.02  # 20ms timeout
            while GPIO.input(self.echo_pin) == 0 and time.perf_counter() < timeout:
                start_time = time.perf_counter()
            
            timeout = time.perf_counter() + 0.02  # 20ms timeout
            while GPIO.input(self.echo_pin) == 1 and time.perf_counter() < timeout:
                stop_time = time.perf_counter()
            
            if start_time and stop_time:
                time_elapsed = stop_time - start_time
                distance = (time_elapsed * 34300) / 2
                return round(distance, 2)
            else:
                return None  # Return None if measurement failed
        except Exception as e:
            glogger.error(f"Error measuring distance: {e}")
            return None
    
    def calculate_volume(self, distance):
        if distance is None:
            return 0
        filled_height = self.mounting_height - distance
        radius = self.pot_diameter / 2
        volume = 3.1416 * (radius ** 2) * filled_height / 1000  # Volume in liters
        return round(volume, 2)
    
    def get_state(self):
        return dict(value=self.value)

@parameters([
    Property.Select(label="Ultrasonic Trig Pin", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="Trigger Pin"),
    Property.Select(label="Ultrasonic Echo Pin", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="Echo Pin"),
    Property.Select(label="Interval", options=[1, 2, 5, 10, 30, 60], description="Measurement Interval in Seconds")
])
class AJ_SR04M_distance(CBPiSensor):
    def __init__(self, cbpi, id, props):
        super(AJ_SR04M_distance, self).__init__(cbpi, id, props)
        self.value = 0
        self.interval = int(self.props.get("Interval", 2))
        self.trig_pin = int(self.props.get("Ultrasonic Trig Pin", 23))
        self.echo_pin = int(self.props.get("Ultrasonic Echo Pin", 24))
        self.pot_diameter = float(self.props.get("Pot Diameter", 40))
        self.mounting_height = float(self.props.get("Mounting Height", 50))
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    async def run(self):
        while self.running:            
            self.value = self.measure_distance()
            # self.log_data(self.value)
            self.push_update(self.value)
            await asyncio.sleep(self.interval)

    def measure_distance(self):
        try:
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            
            start_time, stop_time = None, None
            
            timeout = time.perf_counter() + 0.02  # 20ms timeout
            while GPIO.input(self.echo_pin) == 0 and time.perf_counter() < timeout:
                start_time = time.perf_counter()
            
            timeout = time.perf_counter() + 0.02  # 20ms timeout
            while GPIO.input(self.echo_pin) == 1 and time.perf_counter() < timeout:
                stop_time = time.perf_counter()
            
            if start_time and stop_time:
                time_elapsed = stop_time - start_time
                distance = (time_elapsed * 34300) / 2
                return round(distance, 2)
            else:
                return None  # Return None if measurement failed
        except Exception as e:
            glogger.error(f"Error measuring distance: {e}")
            return None    
    
    def get_state(self):
        return dict(value=self.value)        

def setup(cbpi):
    cbpi.plugin.register("SR04M Volume", AJ_SR04M_volume)
    cbpi.plugin.register("SR04M Volume", AJ_SR04M_distance)
