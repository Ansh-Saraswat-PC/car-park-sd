import heapq
from typing import Dict, List, Optional
from src.models.vehicle import Vehicle
from src.models.spot import ParkingSpot
from src.utils.enums import VehicleType, SpotType

class ParkingFloor:
    def __init__(self, floor_num: int, num_motorcycle: int, num_compact: int, num_large: int):
        self.floor_num = floor_num
        
        # Min-heaps to track available spots by their ID (closest to entrance first)
        self.free_spots: Dict[SpotType, List[int]] = {
            SpotType.MOTORCYCLE: [],
            SpotType.COMPACT: [],
            SpotType.LARGE: []
        }
        
        # Dictionary for O(1) lookup of the actual ParkingSpot object by ID
        self.spots: Dict[int, ParkingSpot] = {}
        
        spot_id_counter = 1
        
        # Helper to initialize spots and push them into the heap
        def init_spots(count: int, spot_type: SpotType):
            nonlocal spot_id_counter
            for _ in range(count):
                spot = ParkingSpot(self.floor_num, spot_id_counter, spot_type)
                self.spots[spot_id_counter] = spot
                heapq.heappush(self.free_spots[spot_type], spot_id_counter)
                spot_id_counter += 1

        init_spots(num_motorcycle, SpotType.MOTORCYCLE)
        init_spots(num_compact, SpotType.COMPACT)
        init_spots(num_large, SpotType.LARGE)

    def _get_allowed_spot_types(self, vehicle_type: VehicleType) -> List[SpotType]:
        if vehicle_type == VehicleType.MOTORCYCLE:
            return [SpotType.MOTORCYCLE, SpotType.COMPACT, SpotType.LARGE]
        elif vehicle_type == VehicleType.CAR:
            return [SpotType.COMPACT, SpotType.LARGE]
        elif vehicle_type == VehicleType.TRUCK:
            return [SpotType.LARGE]
        return []

    def find_and_park(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        allowed_types = self._get_allowed_spot_types(vehicle.vehicle_type)
        
        for spot_type in allowed_types:
            if self.free_spots[spot_type]:
                # O(log N) to pop the nearest spot ID from the heap
                nearest_spot_id = heapq.heappop(self.free_spots[spot_type])
                spot = self.spots[nearest_spot_id]
                spot.assign_vehicle(vehicle)
                return spot
        return None # No spots available on this floor

    def free_spot(self, spot: ParkingSpot):
        spot.remove_vehicle()
        # O(log N) push to make the spot available again
        heapq.heappush(self.free_spots[spot.spot_type], spot.spot_id)