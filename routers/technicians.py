from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from deps.auth_cookie import require_role
from models.user import RoleEnum
from core.pdf import build_invoice_pdf
from core.emailer import send_mail

technicians_router = APIRouter()

class InvoiceItem(BaseModel):
    desc: str
    qty: float
    rate: float

class InvoiceRequest(BaseModel):
    invoiceNumber: str
    issuerName: str
    issuerAddress: str
    recipientName: str
    recipientAddress: str
    recipientEmail: EmailStr
    vatMode: str = "U19"  # "KLE" oder "U19"
    items: List[InvoiceItem]

@technicians_router.post("/invoices")
def create_and_send_invoice(payload: InvoiceRequest, current=Depends(require_role(RoleEnum.TECHNICIAN))):
    pdf = build_invoice_pdf(
        invoice_number=payload.invoiceNumber,
        issuer_name=payload.issuerName,
        issuer_address=payload.issuerAddress,
        recipient_name=payload.recipientName,
        recipient_address=payload.recipientAddress,
        items=[i.dict() for i in payload.items],
        vat_mode=payload.vatMode,
    )
    filename = f"Rechnung_{payload.invoiceNumber}.pdf"
    send_mail(
        subject=f"Rechnung {payload.invoiceNumber}",
        to=payload.recipientEmail,
        body="Guten Tag,\nim Anhang finden Sie Ihre Rechnung.\n\nMit freundlichen Grüßen\nTKND",
        attachment=(filename, pdf),
    )
    return {"ok": True, "sent_to": payload.recipientEmail}
