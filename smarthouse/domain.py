
import random
from datetime import datetime

class SmartHouse:
    def __init__(self, name):
        self.name = name
        self.building = Building(name)
        self.devices = []
        self.floors = []

    def register_floor(self, level):
        floor = Floor(level)
        self.building.add_floor(floor)
        return floor

    def register_room(self, floor, size, name):
        room = Room(size, name)
        floor.add_room(room)
        return room

    def register_device(self, room, device):
        room.add_device(device)
        self.devices.append(device)

    def get_rooms(self):
        rooms = []
        for floor in self.building.floors:
            rooms.extend(floor.rooms)
        return rooms

    def get_devices(self):
        return self.devices


# Beholder de øvrige klassene: Floor, Room, Building, etc.
class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

class Room:
    def __init__(self, room_id, floor, area, room_name):
        self.room_id = room_id  # Legg til room_id
        self.floor = floor  # Legg til floor
        self.area = area  # Legg til area
        self.room_name = room_name  # Legg til room_name
        self.devices = []  # Fortsatt en liste for devices

    def add_device(self, device):
        self.devices.append(device)

class Building:
    def __init__(self, name):
        self.name = name
        self.floors = []

    def add_floor(self, floor):
        self.floors.append(floor)

# Device-klasse for Sensor og Actuator
class Device:
    def __init__(self, id, supplier, model_name, device_type, room=None):
        self.id = id
        self.supplier = supplier
        self.model_name = model_name
        self.device_type = device_type
        self.room = room

    def is_sensor(self):
        return isinstance(self, Sensor)

    def is_actuator(self):
        return isinstance(self, Actuator)

    def get_device_type(self):
        return self.device_type


class Sensor(Device):
    def __init__(self, id, supplier, model_name, device_type, unit, room=None):
        super().__init__(id, supplier, model_name, device_type, room)
        self.unit = unit
        self.measurements = []

    def last_measurement(self):
        if self.measurements:
            return self.measurements[-1]
        return self.generate_measurement()

    def generate_measurement(self):
        timestamp = datetime.now().isoformat()
        value = round(random.uniform(15.0, 25.0), 2)  # Simulerer temperaturmåling
        measurement = Measurement(timestamp, value, self.unit)
        self.measurements.append(measurement)
        return measurement


class Actuator(Device):
    def __init__(self, id, supplier, model_name, device_type, room=None):
        super().__init__(id, supplier, model_name, device_type, room)
        self.active = False
        self.target_value = None

    def turn_on(self, value=None):
        self.active = True
        if value is not None:
            self.target_value = value

    def turn_off(self):
        self.active = False
        self.target_value = None

    def is_active(self):
        return self.active


class Measurement:
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit
