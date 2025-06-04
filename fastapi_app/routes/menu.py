from fastapi import APIRouter
from fastapi_app.models.menu import MenuItem


router = APIRouter()

@router.get("/", tags=["Menu"])
def get_menu_items():
    items = MenuItem.get_all_items()
    return [item.to_dict() for item in items]
