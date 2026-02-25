from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter
import io

def create_watermark_page(page_width, page_height, text="CONFIDENTIAL"):
    packet = io.BytesIO()
    
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # Light transparent watermark
    c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.25))
    
    # Font size relative to page size (dynamic scaling)
    font_size = min(page_width, page_height) / 8
    c.setFont("Helvetica", font_size)

    c.saveState()
    c.translate(page_width/2, page_height/2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()

    c.save()
    
    packet.seek(0)
    return PdfReader(packet).pages[0]


def add_watermark_dynamic(input_pdf, output_pdf, text="CONFIDENTIAL"):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        watermark_page = create_watermark_page(width, height, text)
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

add_watermark_dynamic("input1.pdf", "output_watermarked1.pdf", "CONFIDENTIAL")