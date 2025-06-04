from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi_app.models.payment import Payment
from fastapi_app.models.order import Order


router = APIRouter()

# ✅ POST - Make a Payment (Supports both JSON and FormData)
@router.post("/payment", tags=["Payment"])
async def make_payment(request: Request):
    try:
        # Determine content type and extract payment details
        if request.headers.get("content-type", "").startswith("application/json"):
            data = await request.json()
            order_id = data.get("order_id")
            amount = float(data.get("amount"))
            method = data.get("method")
        else:
            form = await request.form()
            order_id = form.get("order_id")
            amount = float(form.get("amount"))
            method = form.get("method")

        # Validating received payment details
        print(f"🧾 Received payment for Order ID: {order_id}, Amount: {amount}, Method: {method}")

        if not order_id or not amount or not method:
            raise HTTPException(status_code=400, detail="Missing payment details.")

        # Validate order
        order = Order.get_order_by_id(order_id)
        if not order:
            print(f"❌ Order ID {order_id} not found.")
            raise HTTPException(status_code=404, detail="Order not found.")

        # Check if amount matches order total
        if float(amount) != float(order.total_price):
            print(f"❌ Amount mismatch. Given: {amount}, Expected: {order.total_price}")
            raise HTTPException(status_code=400, detail="Amount doesn't match order total.")

        # Validate payment method
        valid_methods = ["UPI", "Card", "Cash"]
        if method not in valid_methods:
            raise HTTPException(status_code=400, detail=f"Invalid payment method: {method}")

        # Create payment
        payment = Payment.create_payment(order_id, amount, method)
        if not payment:
            raise HTTPException(status_code=500, detail="Failed to process payment.")

        # Return success response
        return JSONResponse(content={
            "message": "✅ Payment successful!",
            "payment_id": payment.payment_id,
            "order_id": payment.order_id,
            "amount": round(payment.amount, 2),
            "method": payment.method,
            "status": payment.status,
        })

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"❌ Unhandled exception in make_payment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"❌ Server Error: {str(e)}")


# ✅ GET - List all Payments
@router.get("/payment", tags=["Payment"])
def list_payments():
    try:
        payments = Payment.get_all_payments()
        return [p.to_dict() for p in payments]

    except Exception as e:
        print(f"❌ Unhandled exception in list_payments: {str(e)}")
        raise HTTPException(status_code=500, detail=f"❌ Failed to fetch payments: {str(e)}")
