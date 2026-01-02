from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
import enum
from sqlalchemy.orm import relationship
from core.database import Base

class TicketStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    customer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_tech_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
