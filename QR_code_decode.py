# Decode a QRCode
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('C:/Users/Laura Luna/Documents/Laura/Python_Prog/Nova/myqrcode.png')

result = decode(img)

print(result)