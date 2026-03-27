from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
from typing import List
from .billing import CartItem, CartTotals


def generate_invoice_pdf(file_path: str, sale_id: int, items: List[CartItem], totals: CartTotals) -> None:
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 30 * mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, y, f"Invoice #{sale_id}")
    y -= 10 * mm
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Items:")
    y -= 8 * mm
    c.setFont("Helvetica", 10)
    for item in items:
        c.drawString(20 * mm, y, f"{item.name} x{item.quantity} @ {item.unit_price:.2f}")
        c.drawRightString(180 * mm, y, f"{item.total:.2f} {totals.currency}")
        y -= 6 * mm
        if y < 40 * mm:
            c.showPage()
            y = height - 30 * mm

    y -= 4 * mm
    c.line(20 * mm, y, 180 * mm, y)
    y -= 8 * mm

    c.drawString(120 * mm, y, "Subtotal:")
    c.drawRightString(180 * mm, y, f"{totals.subtotal:.2f} {totals.currency}")
    y -= 6 * mm
    c.drawString(120 * mm, y, "Discount:")
    c.drawRightString(180 * mm, y, f"-{totals.discount:.2f} {totals.currency}")
    y -= 6 * mm
    c.drawString(120 * mm, y, "Tax:")
    c.drawRightString(180 * mm, y, f"{totals.tax:.2f} {totals.currency}")
    y -= 6 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(120 * mm, y, "Total:")
    c.drawRightString(180 * mm, y, f"{totals.total:.2f} {totals.currency}")

    c.showPage()
    c.save()