from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from database import Base


class DCR(Base):
  __tablename__ = "DCR"

  id = Column(Integer, primary_key=True, nullable=False)
  language = Column(String, nullable=False)
  source = Column(String, nullable=False)
  ticket_number = Column(String, nullable=False)
  calls = Column(Integer, server_default="0")
  emails = Column(Integer, server_default="0")
  chats = Column(Integer, server_default="0")
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')

  owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

  # below wee are defining a new relashionship for the User model
  # this will retrieve all the details about user
  owner = relationship("User")

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')


class Vote(Base):
  __tablename__ = "votes"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  dcr_id = Column(Integer, ForeignKey("DCR.id", ondelete="CASCADE"), primary_key=True)
