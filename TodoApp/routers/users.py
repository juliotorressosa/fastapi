from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Query,status
from starlette import status
from database import SessionLocal
from models import Todos, Users
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def change_password():
    return 'the password has changed'


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str=Field(min_length=6)
 
@router.get("/users",status_code=status.HTTP_200_OK)
async def get_user_information(db:db_dependency,user:user_dependency,user_id:int=Path(gt=0)):
    if user_id is None:
        raise HTTPException(status_code=404,detail='User not found.')
    return db.query(Users).filter(Users.id==user_id).first()

@router.put("/password_update",status_code=status.HTTP_204_NO_CONTENT)
async def update_users_password(user:user_dependency,db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='User not found')
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed):
        raise HTTPException(status_code=401,detail='Error on password update intent')
    user_model.hashed = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    