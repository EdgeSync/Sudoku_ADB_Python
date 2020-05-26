from ppadb.client import Client
from PIL import Image
import time
import pytesseract
import io
import numpy as np

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

class Solver:
    def __init__(self):
        self.all_grids = []
        # Default is "127.0.0.1" and 5037
        client = Client(host="127.0.0.1", port=5037)
        self.device = client.devices()[0]

    def get_screen(self):
        screenshot = self.device.screencap()
        with open("screen.png", "wb") as f:
            f.write(screenshot)
        f.close()

    def get_sudoku_grid(self):
        sudoku_boundary = [18, 281, 1062, 1327]
        master = Image.open("screen.png")
        im = master.crop(sudoku_boundary)
        im.save('sudoku.png', 'PNG')

        line_coord = {"1": [0, 4, 1044, 110],
                      "2": [0, 120, 1044, 226],
                      "3": [0, 236, 1044, 342],
                      "4": [0, 352, 1044, 458],
                      "5": [0, 468, 1044, 574],
                      "6": [0, 584, 1044, 690],
                      "7": [0, 700, 1044, 806],
                      "8": [0, 816, 1044, 922],
                      "9": [0, 932, 1044, 1038]}

        master = Image.open("sudoku.png")
        for i in range(1, 10):
            grid = []
            im = master.crop(line_coord[str(i)])
            im.save('box.png', 'PNG')
            # im.show()
            image = Image.open('box.png')
            num_coord = {"1": [10, 5, 110, 105], "2": [125, 5, 220, 105], "3": [235, 5, 335, 105],
                         "4": [355, 5, 445, 105], "5": [475, 5, 565, 105], "6": [585, 5, 685, 105],
                         "7": [705, 5, 795, 105], "8": [825, 5, 915, 105], "9": [935, 5, 1035, 105]}

            for j in range(1, 10):
                im2 = image.crop(num_coord[str(j)])
                imgByteArr = io.BytesIO()
                im2.save(imgByteArr, format='PNG')
                imgByteArr = imgByteArr.getvalue()
                text = pytesseract.image_to_string(Image.open(io.BytesIO(imgByteArr)), config='--psm 13 --oem 0 -c tessedit_char_whitelist=123456789')

                try:
                    text = int(text)
                except:
                    text = 0

                grid.append(text)
            # print("Row {} Done!".format(i))
            self.all_grids.append(grid)

        # print(self.all_grids)
        # print("GOT SUDOKU GRID")

    def find_empty(self):
        for i in range(len(self.all_grids)):
            for j in range(len(self.all_grids[0])):
                if self.all_grids[i][j] == 0:
                    return i, j
        return None

    def valid(self, num, pos):
        # check row
        for i in range(len(self.all_grids[0])):
            if self.all_grids[pos[0]][i] == num and pos[1] != i:
                return False

        # check column
        for i in range(len(self.all_grids[0])):
            if self.all_grids[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.all_grids[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.all_grids[row][col] = i

                if self.solve():
                    return True
                self.all_grids[row][col] = 0


    def enter_answers(self):
        pos = [0, 0]
        for row in self.all_grids:
            pos[0] = 0
            for num in row:
                self.enter_solution(num, pos)
                pos[0] = pos[0]+1
            pos[1] = pos[1]+1

    def enter_solution(self, num, pos):
        x = [78, 192, 309, 423, 543, 660, 765, 882, 1005]
        y = [330, 456, 564, 696, 798, 912, 1029, 1155, 1266]
        num_coords = {1: [87, 1680], 2: [195, 1680], 3: [318, 1680], 4: [429, 1680], 5: [543, 1680],
                      6: [657, 1680], 7: [771, 1680], 8: [879, 1680], 9: [996, 1680]}

        # print("Touching Pos: {} {}".format(x[pos[0]], y[pos[1]]))
        self.device.shell("input touchscreen tap {} {}".format(x[pos[0]], y[pos[1]]))

        # print("Pressing Num: {}".format(num))
        self.device.shell("input touchscreen tap {} {}".format(num_coords[num][0], num_coords[num][1]))


def main():
    s = Solver()
    s.get_screen()
    print("=" * 32 + "\nEnumerating Sudoku Numbers...\n" + "=" * 32)
    s.get_sudoku_grid()
    print("=" * 32 + "\nSolving Sudoku....\n" + "=" * 32)
    s.solve()
    print("="*32 + "\nSOLVED\n" + "="*32)
    print(np.matrix(s.all_grids))
    print("=" * 32 + "\nInputting Answers...\n" + "=" * 32)
    s.enter_answers()

if __name__ == "__main__":
    main()
