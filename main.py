from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import routes from fastapi_app.routes package
from fastapi_app.routes import auth, menu, order, payment, analytics, ml_routes, booking_routes, track, recommend

# Initialize FastAPI app
app = FastAPI(
    title="Restaurant Ordering System",
    description="A FastAPI backend integrated with a Flask ML microservice.",
    version="1.0.0"
)

# Enable CORS for frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to static files relative to this file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend folder
STATIC_DIR = os.path.join(BASE_DIR, "static")          # backend/static folder

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"✅ Serving static files from: {STATIC_DIR}")
else:
    print("⚠️ Warning: Static directory not found. Static files may not be served.")

# Register API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/order", tags=["Order"])
app.include_router(payment.router, tags=["Payment"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(ml_routes.ml_router, prefix="/ml", tags=["Machine Learning"])
app.include_router(booking_routes.router, prefix="/booking", tags=["Table Booking"])
app.include_router(track.router, prefix="/track", tags=["Order Tracking"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])

# Root API endpoint for health check
@app.get("/api")
def root():
    return {"message": "🍽️ DineFlow Backend is Running"}
