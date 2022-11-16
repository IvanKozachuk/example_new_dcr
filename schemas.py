from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class DCR(BaseModel):
    language: str
    source: str
    ticket_number: str
    emails: Optional[int] = 0
    calls: Optional[int] = 0
    chats: Optional[int] = 0

class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

class DCRResponse(DCR):
    created_at: datetime
    owner_id: int
    # owner is returning a new property (pydentic model of UserOut)
    owner: UserOut

    # to automaticaly convert to dict and avoid error during API calling
    class Config:
        orm_mode = True

class DCROut(BaseModel):
  DCR: DCRResponse
  votes: int

  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None


class Vote(BaseModel):
  dcr_id: int
  dir: conint(le=1)