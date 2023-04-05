from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth2 import get_current_user
from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay, UserBase

router = APIRouter(
    prefix='/article',
    tags=['article']
)


# create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)


# read article
@router.get('/{article_id}')  # , response_model=ArticleDisplay)
def get_article_by_id(article_id: int, db: Session = Depends(get_db),
                      current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, article_id),
        'user': current_user
    }
