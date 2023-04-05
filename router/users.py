from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth2 import get_current_user
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# read user
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db),
                  current_user: UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)


@router.get('/{user_id}', response_model=UserDisplay)
def get_user_by_id(user_id: int, db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    return db_user.get_user_by_id(db, user_id)


# update user
@router.post('/{user_id}/update')
def update_user(request: UserBase, user_id: int, db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return db_user.update_user(db, user_id, request)


# delete user
@router.delete('/{user_id}/delete')
def delete_user(user_id, db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, user_id)
