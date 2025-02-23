import unittest
from symtable import Class

from smarthouse.domain import SmartHouse, Sensor, Actuator

class TestSmartHouse(unittest.TestCase):

# Initialiser demo_house (SmartHouse-objektet)
    demo_house = SmartHouse(name= "Demo House")

# Registrer etasjer
    ground_floor = demo_house.register_floor(0)
    second_floor = demo_house.register_floor(1)

# Registrer rom på bakkeplan (Ground floor)
    entrance = demo_house.register_room(ground_floor, 13.5, "Entrance")
    living_room = demo_house.register_room(ground_floor, 20, "Living Room")
    kitchen = demo_house.register_room(ground_floor, 15, "Kitchen")

# Registrer rom på andre etasje (Second floor)
    bedroom_1 = demo_house.register_room(second_floor, 15, "Bedroom 1")
    bathroom = demo_house.register_room(second_floor, 12, "Bathroom")

# Opprett enheter (sensorer og aktuatorer)
    smart_plug = Actuator("A01", "PlugCo", "SmartPlug", "Plug")
    temperature_sensor = Sensor("S01", "SensorCo", "TempSensor", "Temperature", "°C")

# Registrer enhetene i rommene
    demo_house.register_device(entrance, smart_plug)  # Smart plug i entréen
    demo_house.register_device(living_room, temperature_sensor)  # Temperaturmåler i stuen

# Skriv ut informasjon om husstrukturen og enhetene
    print(f"House has {len(demo_house.floors)} floors.")
    for floor in demo_house.building.floors:
     print(f"Floor {floor.level}:")
     for room in floor.rooms:
        print(f"  Room: {room.name}, Size: {room.size} m²")
        for device in room.devices:
            print(f"    Device: {device.model_name} ({device.device_type})")

        def test_smart_plug_device(self):
            smart_plug = Actuator("A01", "PlugCo", "SmartPlug", "Plug")
            self.assertEqual(smart_plug.device_type, "Plug")
            self.assertTrue(isinstance(smart_plug, Actuator))

        def test_temperature_sensor(self):
            temperature_sensor = Sensor("S01", "SensorCo", "TempSensor", "Temperature", "°C")
            self.assertEqual(temperature_sensor.device_type, "Temperature")
            self.assertEqual(temperature_sensor.unit, "°C")

        def test_register_multiple_floors(self):
            demo_house = SmartHouse(name="Demo House")
            ground_floor = demo_house.register_floor(0)
            second_floor = demo_house.register_floor(1)
            self.assertEqual(len(demo_house.building.floors), 2)

        def test_register_room_on_floor(self):
            demo_house = SmartHouse(name="Demo House")
            ground_floor = demo_house.register_floor(0)
            living_room = demo_house.register_room(ground_floor, 20, "Living Room")
            self.assertEqual(len(ground_floor.rooms), 1)
            self.assertEqual(living_room.name, "Living Room")

        def test_device_in_room(self):
            demo_house = SmartHouse(name="Demo House")
            ground_floor = demo_house.register_floor(0)
            living_room = demo_house.register_room(ground_floor, 20, "Living Room")
            smart_plug = Actuator("A01", "PlugCo", "SmartPlug", "Plug")
            demo_house.register_device(living_room, smart_plug)
            self.assertIn(smart_plug, living_room.devices)

        def test_sensor_measurement(self):
            temperature_sensor = Sensor("S01", "SensorCo", "TempSensor", "Temperature", "°C")
            measurement = temperature_sensor.last_measurement()
            self.assertIsNotNone(measurement.value)
            self.assertEqual(measurement.unit, "°C")

        def test_turn_on_actuator(self):
            actuator = Actuator("A01", "PlugCo", "SmartPlug", "Plug")
            actuator.turn_on()
            self.assertTrue(actuator.is_active())

        def test_turn_off_actuator(self):
            actuator = Actuator("A01", "PlugCo", "SmartPlug", "Plug")
            actuator.turn_off()
            self.assertFalse(actuator.is_active())


if __name__ == '__main__':
    unittest.main()