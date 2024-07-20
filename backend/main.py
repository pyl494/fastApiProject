from fastapi import (APIRouter, FastAPI, Depends, HTTPException, Response, status, Form)
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from backend import crud, models, schemas, database
from backend.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder

router_main = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_main.post("/create_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router_main.get("/")
async def root():
    return {"message": "Hello World"}


@router_main.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# login for user, parameter: email, password
@router_main.post("/login")
async def login_user(request: Request, response: Response, user: schemas.UserLogin, db: Session = Depends(get_db)):
    # check if email exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        return JSONResponse(content=jsonable_encoder("Email not found"), status_code=status.HTTP_400_BAD_REQUEST)
        # raise HTTPException(status_code=404, detail="Email not found")
    # check if password is correct
    if not crud.verify_password(user.password, db_user.password):
        return JSONResponse(content=jsonable_encoder("Password incorrect"), status_code=status.HTTP_400_BAD_REQUEST)
        # raise HTTPException(status_code=400, detail="Password incorrect")

    # return user info by json
    return JSONResponse(content=jsonable_encoder(db_user), status_code=status.HTTP_200_OK)


# search user by multi conditions, parameter: id, name, surname, phone, email, user_type
@router_main.post("/search_users")
async def search_users(id: Optional[int] = Form(None), name: Optional[str] = Form(None),
                       surname: Optional[str] = Form(None), phone: Optional[str] = Form(None),
                       email: Optional[str] = Form(None), user_type: Optional[str] = Form(None),
                       db: Session = Depends(get_db)):
    # 在这里处理收到的用户名和密码
    user = crud.search_users(db, id=id, name=name, surname=surname, phone=phone, email=email, user_type=user_type)
    # 可以在这里添加处理逻辑，比如验证用户信息，存储到数据库等
    return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_200_OK)
