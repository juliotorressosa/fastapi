from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Query,status
from starlette import status
from database import SessionLocal
from models import Todos, Users
from pydantic import BaseModel,Field
from .auth import get_current_user


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

class CreateUserRequest(BaseModel):
    username: str
    email:str
    first_name:str
    last_name: str
    password: str
    isactive: bool
    role:str
 
db_dependency = Annotated[Session,Depends(get_db)]   


@router.get("/users")
async def get_user_information():
    return 'the user informations'

@router.put("/users/{user_id}")
async def update_users_password(user_id):
    return 'Password updated'