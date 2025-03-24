import sqlite3
from pathlib import Path


class SmartHouseRepository:
    def __init__(self, db_path):
        # Sørger for at db_path er en gyldig filbane
        if isinstance(db_path, Path):
            db_path = str(db_path)

        # Åpner en SQLite-tilkobling
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row  # Henter kolonner som nøkkel-verdi

    def load_smarthouse_deep(self):
        # Henter alle rom
        rooms_data = self.db.execute("SELECT id, floor, area, name FROM rooms").fetchall()

        rooms = []
        for room_data in rooms_data:
            # Henter enheter for hvert rom
            devices = self.load_devices(room_data['id'])

            room = {
                'id': room_data['id'],
                'floor': room_data['floor'],
                'area': room_data['area'],
                'name': room_data['name'],
                'devices': devices  # Enheter knyttet til rommet
            }
            rooms.append(room)

        return rooms

    def load_devices(self, room_id):
        # Henter enheter knyttet til et rom
        devices_data = self.db.execute("""
            SELECT id, name, type, room_id 
            FROM devices WHERE room_id = ?
        """, (room_id,)).fetchall()

        devices = []
        for device_data in devices_data:
            # Henter målinger for hver enhet
            measurements = self.load_measurements(device_data['id'])

            device = {
                'id': device_data['id'],
                'name': device_data['name'],
                'type': device_data['type'],
                'measurements': measurements  # Målinger knyttet til enheten
            }
            devices.append(device)

        return devices

    def load_measurements(self, device_id):
        # Henter målinger knyttet til en enhet
        measurements_data = self.db.execute("""
            SELECT timestamp, value, unit 
            FROM measurements WHERE device_id = ?
        """, (device_id,)).fetchall()

        measurements = []
        for measurement_data in measurements_data:
            measurement = {
                'timestamp': measurement_data['timestamp'],
                'value': measurement_data['value'],
                'unit': measurement_data['unit']
            }
            measurements.append(measurement)

        return measurements

    def close(self):
        # Lukker forbindelsen til databasen
        self.db.close()
