from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.hash import Hash
from db.models import DBUsers
from schemas import UserBase


def create_user(db: Session, request: UserBase):
    new_user = DBUsers(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DBUsers).all()


def get_user_by_id(db: Session, user_id):
    user = db.query(DBUsers).filter(DBUsers.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {user_id} not found')
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(DBUsers).filter(DBUsers.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DBUsers).filter(DBUsers.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {id} not found')
    user.update({
        DBUsers.username: request.username,
        DBUsers.email: request.email,
        DBUsers.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'


def delete_user(db: Session, id: int):
    user = db.query(DBUsers).filter(DBUsers.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {id} not found')
    db.delete(user)
    db.commit()
    return 'ok'
