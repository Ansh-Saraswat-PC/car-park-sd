from abc import ABC
from src.utils.enums import VehicleType

class Vehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate
        self._type = None  # Set by subclasses

    @property
    def vehicle_type(self) -> VehicleType:
        return self._type

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate)
        self._type = VehicleType.MOTORCYCLE

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate)
        self._type = VehicleType.CAR

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate)
        self._type = VehicleType.TRUCK