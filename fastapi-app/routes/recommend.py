from fastapi import APIRouter
from pydantic import BaseModel
from models.recommend import get_recommended_items

router = APIRouter()

class TasteRequest(BaseModel):
    item_name: str

class ImageRequest(BaseModel):
    item_name: str

@router.post("/taste")
def recommend_by_taste(request: TasteRequest):
    items = get_recommended_items()
    filtered = [item for item in items if request.item_name.lower() in item['name'].lower()]
    return {"recommended_items": filtered or items}

@router.post("/image")
def recommend_by_image(request: ImageRequest):
    items = get_recommended_items()
    filtered = [item for item in items if request.item_name.lower() in item['name'].lower()]
    return {"recommended_items": filtered or items}
