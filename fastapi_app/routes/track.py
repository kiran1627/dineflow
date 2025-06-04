from fastapi import APIRouter, HTTPException, Body, Path
from pydantic import BaseModel
from typing import List, Literal
from fastapi_app.models.order_track import OrderTrack


router = APIRouter()


class OrderOut(BaseModel):
    order_id: str
    customer_name: str
    user_email: str
    items: str
    total_price: float
    mode: Literal["dine-in", "online"]
    order_type: str
    timestamp: str
    status: str


class ForceBody(BaseModel):
    status: str


@router.get("/orders/{mode}", response_model=List[OrderOut])
async def list_orders(mode: Literal["dine-in", "online"]):
    db_mode = mode.replace("-", "")
    rows = OrderTrack.list_by_mode(db_mode)
    for r in rows:
        r["mode"] = mode
        r["total_price"] = float(r["total_price"])
    return rows

@router.get("/order/{order_id}", response_model=OrderOut)
async def get_order(order_id: str = Path(..., min_length=3)):
    row = OrderTrack.get_one(order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    row = row.copy()
    row["mode"] = row["mode"].replace("dinein", "dine-in")
    row["total_price"] = float(row["total_price"])
    return row

@router.post("/order/{order_id}/advance")
async def advance(order_id: str):
    order = OrderTrack.get_one(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order.get("status", "").lower()
    mode = order.get("mode", "").lower()
    flow = OrderTrack.FLOW.get(mode)

    if not flow:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}")

    if current_status not in flow:
        raise HTTPException(status_code=400, detail=f"Invalid current status: {current_status}")

    if current_status == flow[-1]:
        raise HTTPException(status_code=400, detail=f"Order already at final status: {current_status}")

    new_status = OrderTrack.advance_status(order_id)

    if new_status is None:
        raise HTTPException(status_code=400, detail="Unable to advance status")

    return {
        "message": "Status advanced",
        "order_id": order_id,
        "new_status": new_status
    }

@router.put("/order/{order_id}/status")
async def force(order_id: str, body: ForceBody = Body(...)):
    try:
        ok = OrderTrack.set_status(order_id, body.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid status: {e}")

    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "message": "Status updated",
        "order_id": order_id,
        "new_status": body.status
    }

@router.get("/debug/orders")
async def debug_orders():
    rows = OrderTrack.list_all()
    for r in rows:
        r["mode"] = r["mode"].replace("dinein", "dine-in")
    return rows