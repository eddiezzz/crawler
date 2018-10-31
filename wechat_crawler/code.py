import pytesseract
from PIL import Image

#filename = "/Users/zhengchangshuai/Downloads/c.png"
#filename = "/Users/zhengchangshuai/Downloads/usage.png"
filename = "./c.png"

print("filename:" + filename)
image = Image.open(filename)
image.show()
vcode = pytesseract.image_to_string(image)
print("code result:")
print (vcode)

