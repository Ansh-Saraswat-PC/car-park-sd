from typing import Optional
from src.models.vehicle import Vehicle
from src.utils.enums import SpotType

class ParkingSpot:
    def __init__(self, floor_num: int, spot_id: int, spot_type: SpotType):
        self.floor_num = floor_num
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.vehicle: Optional[Vehicle] = None

    @property
    def is_free(self) -> bool:
        return self.vehicle is None

    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if not self.is_free:
            return False
        self.vehicle = vehicle
        return True

    def remove_vehicle(self) -> Optional[Vehicle]:
        parked_vehicle = self.vehicle
        self.vehicle = None
        return parked_vehicle