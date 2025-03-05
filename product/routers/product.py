from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from product import models, schemas
from product.database import get_db

router = APIRouter(
    tags=["product"],
    prefix="/product",
)


@router.get("/list", response_model=List[schemas.DisplayProduct])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.get("/{product_id}", response_model=schemas.DisplayProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(product_id == models.Product.id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(product_id == models.Product.id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@router.put("/{product_id}", status_code=status.HTTP_202_ACCEPTED)
def update_product(product_id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(product_id == models.Product.id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for key, value in request.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return {"message": "Product updated", "product": product}


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.Product,description="Add a new product")
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
