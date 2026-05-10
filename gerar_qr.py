import qrcode

base_url = "https://qr-higienizacao.onrender.com/equipamento/"

for i in range(1, 6):

    url = f"{base_url}{i}"

    img = qrcode.make(url)

    img.save(f"equipamento_{i}.png")

    print(f"QR Code {i} criado!")