import time
from datetime import datetime, timedelta

# Import models
from src.models.vehicle import Car, Motorcycle, Truck
from src.models.ticket import Ticket
from src.core.floor import ParkingFloor
from src.core.lot import ParkingLot
from src.utils.calculator import PricingEngine

def run_simulation():
    print("=== TechVerse Parking System Initializing ===\n")
    
    # Initialize the Singleton Parking Lot
    lot = ParkingLot()
    
    # Add a couple of floors (e.g., Ground floor, Basement 1)
    print("Setting up Floor 1 and Floor 2...")
    lot.add_floor(ParkingFloor(floor_num=1, num_motorcycle=5, num_compact=5, num_large=2))
    lot.add_floor(ParkingFloor(floor_num=2, num_motorcycle=10, num_compact=10, num_large=5))
    
    # Arrivals (Using UP16 license plates)
    print("\n--- Morning Arrivals ---")
    ansh_bike = Motorcycle("UP16-ANSH-01")
    aryan_car = Car("UP16-ARYN-99")
    raj_car = Car("UP16-RAJJ-55")
    kaustubh_car = Car("UP16-KSTB-22")
    delivery_truck = Truck("UP16-DLVR-00")
    
    vehicles = [ansh_bike, aryan_car, raj_car, kaustubh_car, delivery_truck]
    active_tickets = []
    
    for v in vehicles:
        spot = lot.park_vehicle(v)
        if spot:
            ticket = Ticket(v, spot)
            # Rewind the entry time slightly to simulate elapsed duration for pricing
            ticket.entry_time = datetime.now() - timedelta(hours=3, minutes=15) 
            active_tickets.append(ticket)
            print(f"[ENTRY] {v.license_plate} parked successfully.")
            print(f"        -> {ticket}")
        else:
            print(f"[ENTRY] {v.license_plate} failed to park. Lot Full!")
            
    print("\n[ SYSTEM RUNNING ]... Simulating time passing ...\n")
    time.sleep(1) # Brief pause for effect
            
    # Simulating departures
    print("--- Afternoon Departures ---")
    for ticket in active_tickets:
        # 1. Unpark the vehicle to free up the spot in our Min-Heap
        lot.unpark_vehicle(ticket.allocated_spot)
        
        # 2. Mark the ticket as completed
        ticket.close_ticket()
        
        # 3. Calculate the fee
        fee = PricingEngine.calculate_fee(
            ticket.entry_time, 
            ticket.exit_time, 
            ticket.vehicle.vehicle_type
        )
        ticket.amount_paid = fee
        
        print(f"[EXIT] {ticket.vehicle.license_plate} leaving.")
        print(f"       Time parked: {ticket.exit_time - ticket.entry_time}")
        print(f"       Amount Due: ₹{fee:,.2f}")

if __name__ == "__main__":
    run_simulation()