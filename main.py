from PIL import Image
import pytesseract
import io
import time
import numpy as np

class Solve:
    def __init__(self):
        self.grid = []

    def possible(self, y, x, n):
        for i in range(0, 9):
            if self.grid[y][i] == n:
                return False

        for i in range(0,9):
            if self.grid[i][x] == n:
                return False

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0+i][x0+j] == n:
                    return False
        return True

    def solve(self, grid):
        self.grid = grid
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n):
                            self.grid[y][x] = n
                            self.solve(self.grid)
                            self.grid[y][x] = 0
                    return
            print(np.matrix(self.grid))
        # input("More?")

def main():
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    master = Image.open('sudoku.png')
    # master.show()
    # time.sleep(3)

    identified_numbers = {}
    grid = []
    grid = [[5, 3, 0, 6, 0, 0, 0, 9, 8], [0, 7, 0, 1, 9, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [8, 0, 0, 4, 0, 0, 7, 0, 0], [0, 6, 0, 8, 0, 3, 0, 2, 0], [0, 0, 3, 0, 0, 1, 0, 0, 6], [0, 6, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 1, 9, 0, 8, 0], [2, 8, 0, 0, 0, 5, 0, 7, 9]]


    # options = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    # box_boundaries = {"A": [0, 0, 400, 400], "B": [400, 0, 800, 400], "C": [800, 0, 1200, 400],
    #                   "D": [0, 400, 400, 800], "E": [400, 400, 800, 800], "F": [800, 400, 1200, 800],
    #                   "G": [0, 800, 400, 1200], "H": [400, 800, 800, 1200], "I": [800, 800, 1200, 1200]}
    # # we pick our box
    # for o in options:
    #     values = []
    #     im = master.crop((box_boundaries[o]))
    #     # im.show()
    #     # time.sleep(3)
    #
    #     # save the currently cropped box
    #     im.save('box.png', 'PNG')
    #     image = Image.open('box.png')
    #     box_coord = {"1": [8, 8, 133, 133], "2": [140, 8, 266, 133], "3": [280, 8, 395, 133],
    #                  "4": [8, 140, 133, 266], "5": [140, 140, 266, 266], "6": [270, 140, 399, 266],
    #                  "7": [8, 270, 133, 399], "8": [140, 270, 266, 399], "9": [270, 280, 399, 399]}
    #
    #     for i in range(1, 10):
    #         im2 = image.crop(box_coord[str(i)])
    #         # im2.show()
    #         imgByteArr = io.BytesIO()
    #         im2.save(imgByteArr, format='PNG')
    #         imgByteArr = imgByteArr.getvalue()
    #
    #         text = pytesseract.image_to_string(Image.open(io.BytesIO(imgByteArr)), lang='eng',
    #                                            config='--psm 13 --oem 3 -c tessedit_char_whitelist=123456789')
    #         try:
    #             int(text)
    #         except:
    #             text = 0
    #
    #         values.append(int(text))
    #     identified_numbers[o] = values
    #     grid.append(values)
    #     print("{} Done!".format(o))
    #
    # # print(grid)
    # # print(np.matrix(grid))

    s = Solve()
    s.solve(grid)
    print(np.matrix(s.grid))

if __name__ == "__main__":
    main()
