"""Secure, simple parking-lot booking and manifest example for Lab 5."""

import hashlib
import json
import secrets
from copy import deepcopy
from pathlib import Path


DEFAULT_SLOTS = {
    "P01": {
        "plate": "KA01AB1234", "hours": 2, "rate": 20.0, "is_occupied": True
    },
    "P02": {
        "plate": "TN07CD5678", "hours": 0, "rate": 20.0, "is_occupied": False
    },
    "P03": {
        "plate": "MH02EF9012", "hours": 4, "rate": 30.0, "is_occupied": True
    },
}


class ParkingLot:
    """Store parking slots, track bookings, and export the current manifest."""

    def __init__(self, slots):
        """Copy slots to ensure each parking lot has independent state."""
        self.slots = deepcopy(slots)
        self.total_collections = 0.0

    def park_vehicle(self, slot_id, plate_no, hours_booked=1, entry_logs=None):
        """Book a free slot and optionally record an entry in a log."""
        if not isinstance(hours_booked, int) or hours_booked <= 0:
            raise ValueError("Booking duration must be a positive integer")
        slot = self.slots.get(slot_id)
        if slot is None or slot["is_occupied"]:
            return False
        slot["plate"] = plate_no
        slot["hours"] = hours_booked
        slot["is_occupied"] = True
        self.total_collections += slot["rate"] * hours_booked
        if entry_logs is not None:
            entry_logs.append(
                f"Vehicle {plate_no} parked at slot {slot_id} "
                f"for {hours_booked} hours with total charge calculated"
            )
        return True

    def release_slot(self, slot_id):
        """Clear an occupied slot and report whether it was released."""
        slot = self.slots.get(slot_id)
        if slot is None or not slot["is_occupied"]:
            return False
        slot.update({"plate": "", "hours": 0, "is_occupied": False})
        return True

    def check_slot_availability(self, slot_id):
        """Return whether the requested slot exists and is available."""
        slot = self.slots.get(slot_id)
        return slot is not None and not slot["is_occupied"]

    def calculate_parking_fee(self, slot_id, surge_multiplier=1.0):
        """Calculate the slot's hourly fee using a numeric surge factor."""
        if (
            not isinstance(surge_multiplier, (int, float))
            or surge_multiplier < 0
        ):
            raise ValueError("Surge multiplier must be a nonnegative number")
        base_rate = self.slots[slot_id]["rate"]
        return round(base_rate * surge_multiplier, 2)

    @staticmethod
    def generate_vehicle_hash(plate_no):
        """Return a SHA-256 digest of a registration number."""
        return hashlib.sha256(plate_no.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_ticket_pin():
        """Create a secure four-digit ticket PIN."""
        return 1000 + secrets.randbelow(9000)

    def export_parking_manifest(self, filename="parking_manifest.txt"):
        """Write the current parking slots as readable JSON."""
        destination = Path(filename)
        destination.write_text(
            json.dumps(self.slots, indent=2) + "\n", encoding="utf-8"
        )
        print("Parking manifest exported to:", destination)

    def get_available_summary(self):
        """Count available parking slots."""
        return sum(not slot["is_occupied"] for slot in self.slots.values())


def main():
    """Demonstrate booking, release, fee calculation, hashing, and export."""
    parking_lot = ParkingLot(DEFAULT_SLOTS)
    parking_lot.park_vehicle("P02", "DL03GH3456", 3)
    parking_lot.release_slot("P01")
    print("Is P02 available:", parking_lot.check_slot_availability("P02"))
    print("Surge Parking Fee:", parking_lot.calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", parking_lot.generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", parking_lot.generate_ticket_pin())
    parking_lot.export_parking_manifest()
    print("Vacant slots:", parking_lot.get_available_summary())
    print("Total collections:", parking_lot.total_collections)


if __name__ == "__main__":
    main()
