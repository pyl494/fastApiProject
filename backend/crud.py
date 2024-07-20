from sqlalchemy.orm import Session
from backend import models, schemas
from passlib.context import CryptContext

# pip install fastapi uvicorn sqlalchemy pymysql alembic passlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# check user exist or not by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        password=hashed_password,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def search_users(db: Session, id: int = None, name: str = None, surname: str = None, phone: str = None, email: str = None, user_type: str = None):
    query = db.query(models.User)
    if id:
        query = query.filter(models.User.id == id)
    if name:
        query = query.filter(models.User.name.like(f"%{name}%"))
    if surname:
        query = query.filter(models.User.surname.like(f"%{surname}%"))
    if phone:
        query = query.filter(models.User.phone.like(f"%{phone}%"))
    if email:
        query = query.filter(models.User.email.like(f"%{email}%"))
    if user_type != "all":
        query = query.filter(models.User.user_type == user_type)
    return query.all()

