from smarthouse.domain import SmartHouse, Sensor, Actuator, Room, Floor, Measurement

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
print(f"House has {len(demo_house.building.floors)} floors.")
for floor in demo_house.building.floors:
    print(f"Floor {floor.level}:")
    for room in floor.rooms:
        print(f"  Room: {room.name}, Size: {room.size} m²")
        for device in room.devices:
            print(f"    Device: {device.model_name} ({device.device_type})")