from passlib.context import CryptContext
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from product import schemas, models
from product.database import get_db


router = APIRouter(
    tags=["seller"],
    prefix="/seller",
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hash_pass = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hash_pass)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
