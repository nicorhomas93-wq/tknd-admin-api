# routers/customers.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from deps.auth_dep import require_role
from models.user import RoleEnum
from models.ticket import Ticket, TicketStatus
from pydantic import BaseModel

customers_router = APIRouter()

class TicketCreate(BaseModel):
    title: str
    description: str | None = None

@customers_router.post("/tickets")
def create_ticket(req: TicketCreate, db: Session = Depends(get_db), current=Depends(require_role(RoleEnum.CUSTOMER))):
    """
    Kunde legt Ticket an (Status: OPEN).
    """
    t = Ticket(title=req.title, description=req.description, customer_user_id=current.id)
    db.add(t); db.commit(); db.refresh(t)
    return {"id": t.id, "status": t.status}

@customers_router.get("/tickets")
def my_tickets(db: Session = Depends(get_db), current=Depends(require_role(RoleEnum.CUSTOMER))):
    """
    Eigene Tickets auflisten.
    """
    q = db.query(Ticket).filter(Ticket.customer_user_id == current.id).order_by(Ticket.id.desc())
    return [{"id": t.id, "title": t.title, "status": t.status} for t in q.all()]
