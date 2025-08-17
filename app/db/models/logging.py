from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db import WithTimeStamp


class Log(WithTimeStamp):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    level = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    object_type = Column(String, nullable=False)
    object_id = Column(Integer, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String, nullable=True)
    message = Column(Text, nullable=True)

    user = relationship("User", back_populates="logs")