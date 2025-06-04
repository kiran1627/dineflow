from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi_app.models.booking import Booking
import uuid

router = APIRouter()

class BookingRequest(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str
    date: str  # format: YYYY-MM-DD
    time: str  # format: HH:MM
    guests: int

@router.post("/book_table")
async def book_table(booking: BookingRequest):
    try:
        if not booking.customer_name.strip():
            raise HTTPException(status_code=400, detail="Customer name is required")
        if booking.guests <= 0:
            raise HTTPException(status_code=400, detail="At least one guest must be specified")

        booking_id = str(uuid.uuid4())
        timestamp = datetime.now()

        success = Booking.save_to_csv(
            booking_id=booking_id,
            customer_name=booking.customer_name,
            email=booking.email,
            phone=booking.phone,
            date=booking.date,
            time=booking.time,
            guests=booking.guests,
            timestamp=timestamp
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save the booking")

        return {"message": "✅ Table booked successfully", "booking_id": booking_id}

    except Exception as e:
        print(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
