from fastapi import APIRouter, HTTPException
import requests

ml_router = APIRouter(prefix="/ml", tags=["ML Services"])
FLASK_URL = "http://localhost:5000/ml"

@ml_router.post("/predict-food")
def forward_food_prediction(image_base64: str):
    try:
        res = requests.post(f"{FLASK_URL}/predict-food", json={"image_base64": image_base64})
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ml_router.get("/forecast-orders")
def forward_order_forecast(date: str):
    try:
        res = requests.get(f"{FLASK_URL}/forecast-orders", params={"date": date})
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ml_router.get("/dynamic-price")
def forward_dynamic_price(item: str, demand: int = 50):
    try:
        res = requests.get(f"{FLASK_URL}/dynamic-price", params={"item": item, "demand": demand})
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ml_router.get("/recommend")
def forward_recommendations(user_id: str):
    try:
        res = requests.get(f"{FLASK_URL}/recommend", params={"user_id": user_id})
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ml_router.post("/analyze-sentiment")
def forward_sentiment_analysis(review: str):
    try:
        res = requests.post(f"{FLASK_URL}/analyze-sentiment", json={"review": review})
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
