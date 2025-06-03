from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Initialize FastAPI app
app = FastAPI(
    title="Restaurant Ordering System",
    description="A FastAPI backend integrated with a Flask ML microservice.",
    version="1.0.0"
)

# Import route modules
from routes import auth, menu, order, payment, analytics, ml_routes, booking_routes, track, recommend

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to your static files and images (your backend static content)
STATIC_DIR = "C:/Users/HP/restaurant-ordering-system/backend/static"
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

if os.path.exists(IMAGES_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"✅ Serving static files from: {IMAGES_DIR}")
else:
    print("⚠️ Warning: 'static/images' directory not found. Static files may not be served.")

# ** NEW ** Serve React frontend build folder as root "/"
REACT_BUILD_DIR = "C:/Users/HP/restaurant-ordering-system/frontend/build"

if os.path.exists(REACT_BUILD_DIR):
    app.mount("/", StaticFiles(directory=REACT_BUILD_DIR, html=True), name="frontend")
    print(f"✅ Serving React frontend from: {REACT_BUILD_DIR}")
else:
    print("⚠️ Warning: React build directory not found. Frontend will not be served.")

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

# Optional: health check or API root endpoint
@app.get("/api")
def root():
    return {"message": "✅ Restaurant Ordering System API is up and running"}
