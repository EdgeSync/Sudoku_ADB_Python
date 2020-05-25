from ppadb.client import Client
from PIL import Image
import time
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

## Default is "127.0.0.1" and 5037
# client = Client(host="127.0.0.1", port=5037)
# device = client.devices()[0]
#
# screenshot = device.screencap()
# with open("screen.png", "wb") as f:
#     f.write(screenshot)
# f.close()

sudoku_boundary = [18, 281, 1062, 1327]

master = Image.open("screen.png")
im = master.crop(sudoku_boundary)
im.save('sudoku.png', 'PNG')

box_coord = {"1": [0, 0, 345, 345], "2": [352, 0, 690, 345], "3": [700, 0, 1035, 345],
             "4": [0, 350, 300, 690], "5": [352, 352, 690, 690], "6": [700, 352, 1035, 690],
             "7": [0, 704, 345, 1035], "8": [352, 704, 690, 1035], "9": [700, 704, 1035, 1035]}

master = Image.open("sudoku.png")
for i in range(1, 2):
    im = master.crop(box_coord[str(i)])
    # im.show()

    im.save('box.png', 'PNG')
    image = Image.open('box.png')
    box_coord = {"1": [20, 12, 100, 100], "2": [120, 8, 210, 103], "3": [250, 8, 325, 100],
                 "4": [20, 135, 100, 210], "5": [120, 130, 220, 220], "6": [240, 130, 340, 220],
                 "7": [10, 252, 110, 330], "8": [120, 252, 220, 330], "9": [240, 252, 340, 330]}

    for i in range(2, 3):
        im2 = image.crop(box_coord[str(i)])
        im2.show()
        # time.sleep(1)
        imgByteArr = io.BytesIO()
        im2.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        text = pytesseract.image_to_string(Image.open(io.BytesIO(imgByteArr)), lang='eng',
               config='--psm 13 --oem 3 -c tessedit_char_whitelist=123456789')


        print(text)
