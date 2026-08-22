from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# What a client sends when registering
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


# What a client sends when logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# What the API sends back — note: no password, no hash
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    # Lets Pydantic read data straight from a SQLAlchemy model object
    model_config = ConfigDict(from_attributes=True)