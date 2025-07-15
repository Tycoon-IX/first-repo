import qrcode

# Buat QR Code
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data("https://www.kamen-rider-official.com/")
qr.make(fit=True)

# Simpan sebagai gambar
img = qr.make_image(fill_color="pink", back_color="white")
img.save("kuuga.png")
print("QR Code disimpan sebagai 'my_qr.png'")