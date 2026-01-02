from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_invoice_pdf(invoice_number: str, issuer_name: str, issuer_address: str,
                      recipient_name: str, recipient_address: str,
                      items: list[dict], vat_mode: str = "U19") -> bytes:
    """
    items: [{ "desc": str, "qty": float, "rate": float }]
    vat_mode: "KLE" (0%) oder "U19" (19%)
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    y = h - 40
    c.setFont("Helvetica-Bold", 14); c.drawString(40, y, f"Rechnung {invoice_number}"); y -= 24
    c.setFont("Helvetica", 10)
    c.drawString(40, y, issuer_name); y -= 14
    for line in issuer_address.splitlines():
        c.drawString(40, y, line); y -= 12

    y -= 10
    c.setFont("Helvetica-Bold", 12); c.drawString(40, y, "Rechnung an:"); y -= 16
    c.setFont("Helvetica", 10); c.drawString(40, y, recipient_name); y -= 14
    for line in recipient_address.splitlines():
        c.drawString(40, y, line); y -= 12

    y -= 10
    c.setFont("Helvetica-Bold", 11); c.drawString(40, y, "Positionen"); y -= 16
    c.setFont("Helvetica", 10)
    net_total = 0.0
    for it in items:
        line = f"{it['desc']}  x{it['qty']}  á {it['rate']:.2f} €"
        c.drawString(40, y, line); y -= 14
        net_total += it["qty"] * it["rate"]

    vat_rate = 0.19 if vat_mode == "U19" else 0.0
    vat = net_total * vat_rate
    gross = net_total + vat

    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, f"Zwischensumme: {net_total:.2f} €"); y -= 14
    c.drawString(40, y, f"USt ({int(vat_rate*100)}%): {vat:.2f} €"); y -= 14
    c.drawString(40, y, f"Gesamt: {gross:.2f} €"); y -= 20

    c.showPage()
    c.save()
    return buf.getvalue()
