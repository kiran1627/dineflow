from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr  # ✅ Use EmailStr
from typing import List
from datetime import datetime
from models.order import Order

router = APIRouter()

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class OrderRequest(BaseModel):
    id: str
    customer_name: str
    user: EmailStr  # ✅ Stronger type check
    items: List[Item]
    total_price: float
    order_type: str
    mode: str
    timestamp: datetime

@router.post("/save_order")
async def save_order(order: OrderRequest):
    try:
        print(f"📩 Received order: {order.dict()}")

        if not order.customer_name.strip():
            raise HTTPException(status_code=400, detail="Missing 'customer_name' field")
        if not order.items:
            raise HTTPException(status_code=400, detail="Missing 'items' field")
        
        # Save order to CSV
        success = Order.save_to_csv(
            order_id=order.id,
            customer_name=order.customer_name,
            user_email=order.user,
            items=[item.dict() for item in order.items],
            total_price=order.total_price,
            mode=order.mode,
            order_type=order.order_type,
            timestamp=order.timestamp
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save the order")

        return {"message": "✅ Order saved successfully", "order_id": order.id}

    except Exception as e:
        print(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
