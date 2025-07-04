from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models, database
from ..schemas import TokenData
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=20

router=APIRouter()

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def generate_token(data: dict):
    from jose import jwt
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login')
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    seller=db.query(models.Seller).filter(models.Seller.username==request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found/invalid user") 

    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    access_token=generate_token(
        data = {"sub": seller.username}
        )
    return {'access_token': access_token, 'token_type': 'bearer'}

def get_current_user(token:str =Depends(oauth2_scheme)):            
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})    
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username:str =payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data= TokenData(username=username)

    except JWTError:
        raise credentials_exception
