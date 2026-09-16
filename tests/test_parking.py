import unittest
from datetime import datetime, timedelta

from src.models.vehicle import Car, Motorcycle, Truck
from src.core.floor import ParkingFloor
from src.core.lot import ParkingLot
from src.utils.calculator import PricingEngine
from src.utils.enums import VehicleType

class TestParkingSystem(unittest.TestCase):
    def setUp(self):
        # Reset the Singleton instance before each test to prevent test pollution
        ParkingLot._instance = None
        self.lot = ParkingLot()
        
        # Create a tiny floor for easy mathematical testing: 2 Bikes, 2 Cars, 1 Truck spot
        self.floor = ParkingFloor(floor_num=1, num_motorcycle=2, num_compact=2, num_large=1)
        self.lot.add_floor(self.floor)

    def test_min_heap_allocation(self):
        """Proves O(1) allocation always gives the lowest spot ID available."""
        car1 = Car("TEST-CAR-1")
        car2 = Car("TEST-CAR-2")
        
        spot1 = self.lot.park_vehicle(car1)
        spot2 = self.lot.park_vehicle(car2)
        
        self.assertIsNotNone(spot1)
        self.assertIsNotNone(spot2)
        self.assertLess(spot1.spot_id, spot2.spot_id, "Heap did not pop the lowest ID first!")

    def test_spot_type_capacity_and_constraints(self):
        """Proves vehicles respect spot types and lot capacity limits."""
        truck1 = Truck("TRK-1")
        truck2 = Truck("TRK-2") # Should fail, only 1 large spot exists
        
        spot1 = self.lot.park_vehicle(truck1)
        spot2 = self.lot.park_vehicle(truck2) 
        
        self.assertIsNotNone(spot1, "First truck should park successfully.")
        self.assertIsNone(spot2, "Second truck parked despite no large spots being available!")

    def test_pricing_engine_minimum_charge(self):
        """Proves the pricing engine enforces a 1-hour minimum charge."""
        # Parked for just 15 minutes
        entry_time = datetime.now() - timedelta(minutes=15)
        exit_time = datetime.now()
        
        fee = PricingEngine.calculate_fee(entry_time, exit_time, VehicleType.CAR)
        self.assertEqual(fee, 50.0, "Minimum charge of ₹50.0 for a car was not enforced.")

    def test_pricing_engine_rounding(self):
        """Proves the pricing engine rounds up to the next hour."""
        # Parked for 1 hour and 5 minutes
        entry_time = datetime.now() - timedelta(hours=1, minutes=5)
        exit_time = datetime.now()
        
        fee = PricingEngine.calculate_fee(entry_time, exit_time, VehicleType.MOTORCYCLE)
        # Should charge for 2 hours (2 * ₹20.0 = ₹40.0)
        self.assertEqual(fee, 40.0, "Pricing did not round up to the next hour correctly.")

if __name__ == '__main__':
    unittest.main()