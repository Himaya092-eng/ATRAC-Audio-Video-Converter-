"""Generate Windows app icon for ATRAC Converter using Pillow.
This ensures the MSI, desktop shortcut and in-app sidebar use one consistent icon.
"""
from PIL import Image, ImageDraw, ImageFilter

S = 512
im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
# Rounded square, deep navy with electric-blue accent
d.rounded_rectangle((16, 16, 496, 496), radius=112, fill=(9, 22, 47, 255), outline=(52, 177, 247, 255), width=16)
d.rounded_rectangle((34, 34, 478, 478), radius=96, outline=(21, 91, 160, 255), width=5)
# Stylized A with cyan top and blue right edge
d.line([(123, 378), (251, 121), (384, 378)], fill=(49, 174, 248, 255), width=62, joint="curve")
d.line([(129, 378), (251, 121)], fill=(114, 230, 255, 255), width=27, joint="curve")
d.line([(187, 298), (319, 298)], fill=(101, 224, 255, 255), width=35)
# Conversion arrow
d.arc((97, 325, 419, 454), 0, 164, fill=(79, 218, 255, 255), width=21)
d.polygon([(386, 381), (442, 413), (384, 433)], fill=(79, 218, 255, 255))
# Waveform bars inside A
for x, height in [(218, 29), (240, 54), (263, 41), (286, 23)]:
    d.rounded_rectangle((x, 270-height, x+11, 270), radius=5, fill=(198, 249, 255, 255))
im.save("ATRAC_v30.ico", format="ICO", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
print("Created ATRAC_v30.ico")
