import uuid
from datetime import datetime
from typing import Optional
from src.models.vehicle import Vehicle
from src.models.spot import ParkingSpot
from src.utils.enums import TicketStatus

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        # Generate a unique 8-character ID for the ticket
        self.ticket_id = str(uuid.uuid4())[:8].upper()
        self.vehicle = vehicle
        self.allocated_spot = spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.status = TicketStatus.ACTIVE
        self.amount_paid = 0.0

    def close_ticket(self):
        """Marks the exit time and updates status when the vehicle leaves."""
        self.exit_time = datetime.now()
        self.status = TicketStatus.COMPLETED

    def __str__(self):
        return (f"Ticket[{self.ticket_id}] - {self.vehicle.license_plate} "
                f"| Floor {self.allocated_spot.floor_num}, Spot {self.allocated_spot.spot_id}")