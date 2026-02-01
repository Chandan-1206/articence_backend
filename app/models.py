from sqlalchemy import Column, String, Enum, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


class CallState(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    PROCESSING_AI = "PROCESSING_AI"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"


class Call(Base):
    __tablename__ = "calls"

    id = Column(String, primary_key=True)
    state = Column(Enum(CallState), nullable=False)

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_id = Column(String, ForeignKey("calls.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
