import math
from datetime import datetime
from src.utils.enums import VehicleType

class PricingEngine:
    # Base hourly rates
    HOURLY_RATES = {
        VehicleType.MOTORCYCLE: 20.0,
        VehicleType.CAR: 50.0,
        VehicleType.TRUCK: 100.0
    }

    @classmethod
    def calculate_fee(cls, entry_time: datetime, exit_time: datetime, vehicle_type: VehicleType) -> float:
        """
        Calculates the parking fee by rounding up to the nearest hour.
        Enforces a minimum charge of 1 hour.
        """
        if not entry_time or not exit_time:
            raise ValueError("Both entry and exit times must be provided.")
            
        time_diff = exit_time - entry_time
        
        # Convert timedelta to total hours, then round up
        hours_parked = math.ceil(time_diff.total_seconds() / 3600)
        
        # Real-world business logic: Minimum charge is always 1 hour
        hours_billed = max(1, hours_parked)
        
        rate = cls.HOURLY_RATES.get(vehicle_type, 50.0)  # Default fallback rate
        
        return hours_billed * rate