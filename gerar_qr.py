import qrcode

url = "http://192.168.7.175:5000/equipamento/1"

img = qrcode.make(url)

img.save("equipamento1.png")

print("QR Code criado com sucesso!")