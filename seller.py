from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models, schemas
from typing import List
from fastapi import FastAPI, status, Response, HTTPException
from passlib.context import CryptContext



router=APIRouter(tags=["Seller"],
                 prefix="/seller")

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/', response_model=schemas.DisplaySeller, tags=["Seller"])
def create_seller(request:schemas.Seller, db:Session=Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller= models.Seller(username=request.username, email=request.email, password=hashedpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller