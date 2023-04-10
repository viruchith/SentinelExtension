import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from .database import Base


class StolenData(Base):
    __tablename__ = "stolen_data"
    id = Column(Integer,primary_key=True)
    url = Column(String)
    title = Column(String)
    form_data = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
