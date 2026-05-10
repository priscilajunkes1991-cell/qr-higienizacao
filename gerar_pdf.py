from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

pdf = canvas.Canvas("etiquetas_qrcode.pdf", pagesize=A4)

largura, altura = A4

logo = ImageReader("static/logo.png")

qrcodes = [
    ("equipamento_1.png", "Equipamento 1"),
    ("equipamento_2.png", "Equipamento 2"),
    ("equipamento_3.png", "Equipamento 3"),
    ("equipamento_4.png", "Equipamento 4"),
    ("equipamento_5.png", "Equipamento 5"),
]

x = 40
y = altura - 170

for arquivo, nome in qrcodes:

    # Fundo da etiqueta
    pdf.roundRect(x - 10, y - 40, 130, 180, 10, stroke=1, fill=0)

    # Logo
    pdf.drawImage(logo, x + 15, y + 90, width=70, height=70, mask='auto')

    # QR Code
    qr = ImageReader(arquivo)
    pdf.drawImage(qr, x, y - 10, width=100, height=100)

    # Nome equipamento
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(x + 50, y - 25, nome)

    x += 170

    if x > 400:
        x = 40
        y -= 220

pdf.save()

print("PDF criado com sucesso!")