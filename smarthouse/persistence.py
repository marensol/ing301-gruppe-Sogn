import copy
import sqlite3
import os
from tabnanny import check
from tkinter.font import names
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Floor, Room, Device

class SmartHouse:
    def_init_(self, name):
        self.name = name
        self.rooms.append(room)

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, db_file):
        try:
            db_path = os.path.abspath(db_file)
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print(f"Error opening database {e}")
            self.conn = None
            self.get_cursor = None

    def __del__(self):
        if self.conn:
            self.conn.close()

    def get_cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    def load_smarthouse_deep(self):
        """
        Denne metoden henter en komplett instans av _SmartHouse_
        objektet som er lagret i denne databasen. Alle refererte objekter
        (f.eks. rom, enheter) hentes også.
        """
        if not self.conn:
            raise ConnectionError("Databaseforbindelsen er ikke opprettet")

        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM `rooms`")
            rooms = cursor.fetchall()

            smarthouse_name = "Mitt Smarthus"
            smarthouse = SmartHouse(name=smarthouse_name)

            # Legg til rommene basert på informasjon fra databasen
            for room in rooms:
                name = room[1]  # Hent romnavn fra databasen
                size = 0  # Sett en standardverdi for size, eller bruk room[2] hvis du har størrelsen i databasen
                room_obj = Room(size=size, name=name)  # Opprett rommet
                smarthouse.add_room(room_obj)  # Legg rommet til SmartHouse

            return smarthouse

        except sqlite3.Error as e:
            print(f"Databasefeil: {e}")
            return None

    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here

        cursor=self.cursor()
        cursor.execute("SELECT * FROM reading WHERE sensor id = ? ORDER BY timestamp DESC LIMIT 1",  (sensor.id))
        latest_reading = cursor.fetchone()
        if latest_reading is None:
            return None

        return Measurement(id=latest_reading[0], value=latest_reading[1], timestamp=latest_reading[2])

    def update_actuator_state(self, actuator):

        cursor=self.repo.get_cursor()

        cursor.execute("SELECT * FROM actuator WHERE id = ? ", (actuator.id,))
        existing_actuators = cursor.fetchone()

        if existing_actuators is None:
            cursor.execute("UPDATE actuator SET state = ? WHERE id = ?", (actuator.state, actuator.id))


        self.conn.commit()







    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.
        pass


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #    SQL statements first in a SQL editor like Dbeaver and then copy it over here.

        cursor=self.repo.get_cursor()

        query = "SELECT AVG(value), DATE(timestamp) FROM measurements WHERE room_id = ? AND type = 'temperature'"

        params = [room.id]
        if from_date:
            query+= "AND timestamp >= ?"
            params.append(from_date)
        if until_date:
            query+= "AND timestamp <= ?"
            params.append(until_date)

        query += "GROUP BY DATE(timestamp)"

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        avg_temperatures = {date: avg_temp for avg_temp, date in results}

        return avg_temperatures

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement

        cursor=self.get_cursor()


        cursor.execute("SELECT AVG(value) FROM measurements WHERE room_id = ? AND type = 'humidity', AND DATE (timestamp)= ?", (room.id, date))
        avg_humidity = cursor.fetchone()[0]

        cursor.execute("""SELECT strftime('%H', timestamp) AS hour, COUNT(*) FROM measurements WHERE room_id = ? AND type = 'humidity' AND DATE(timestamp) GROUP BY hour HAVING COUNT(*)> 3""", (room.id, date, avg_humidity))

        hours_with_humidity= [int(hour) for hour,_ in cursor.fetchall()
                              ]
        return hours_with_humidity

