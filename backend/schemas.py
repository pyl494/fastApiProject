from pydantic import BaseModel, EmailStr
from datetime import datetime, date


class UserCreate(BaseModel):
    name: str
    surname: str
    phone: str
    email: EmailStr
    password: str
    user_type: str


class User(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: EmailStr
    user_type: str
    created_at: datetime

    # 这个设置告诉 Pydantic 在数据模型转换时，要以 ORM 模式处理数据。1. 自动转换数据库模型 2.处理数据库特有的返回数据
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSearch(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: EmailStr
    user_type: str
    # created_at: datetime
    created_at: str

    # from_user 是一个类方法 (@classmethod)，用于从一个 User 对象创建一个 UserSearch 对象。
    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            name=user.name,
            surname=user.surname,
            phone=user.phone,
            email=user.email,
            user_type=user.user_type,
            # created_at=user.created_at,
            # created_at=user.created_at.date()
            created_at=user.created_at.strftime("%Y-%m-%d")  # 格式化为 yyyy-MM-dd 字符串
        )
