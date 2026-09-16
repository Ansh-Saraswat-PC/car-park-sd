from typing import List, Optional
from src.models.vehicle import Vehicle
from src.models.spot import ParkingSpot
from src.core.floor import ParkingFloor

class ParkingLot:
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParkingLot, cls).__new__(cls)
            cls._instance.floors: List[ParkingFloor] = []
        return cls._instance

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in self.floors:
            spot = floor.find_and_park(vehicle)
            if spot:
                return spot
        
        # If we iterate through all floors and find nothing, lot is full
        return None

    def unpark_vehicle(self, spot: ParkingSpot):
        # Find the correct floor using the spot's floor number
        for floor in self.floors:
            if floor.floor_num == spot.floor_num:
                floor.free_spot(spot)
                break