from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/selections")
def get_selections_page(request: Request):
    return templates.TemplateResponse("selections.html", {"request": request})


@router.get("/reviews")
def get_reviews_page(request: Request):
    return templates.TemplateResponse("reviews.html", {"request": request})