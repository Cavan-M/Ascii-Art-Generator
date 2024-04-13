# Turn any image into Acii art!
# The simpler the image, the better the result
# Author: Cavan McLellan
# Date: 2023-04-13

try:
    import halftone as ht
except ModuleNotFoundError:
    import os
    os.system("pip install halftone")
    import halftone as ht
from PIL import Image


class ASCIIArt:
    def __init__(self, filepath, max_width=150):
        self.max_width = max_width
        self.filepath = filepath
        self.output_name = "halftone_img"
        self.image_array = list()
        self.image_matrix = list()
        self.image = None

    def scale_image(self, im1):
        if im1.size[1] > self.max_width:
            new_dimensions = (int(im1.size[0]*0.75), int(im1.size[1]*0.75))
            im2 = im1.resize(new_dimensions)
            self.scale_image(im2)
        else:
            im1.save('resized.bmp')
    def create_halftone(self):
        self.scale_image(Image.open(self.filepath))
        img = Image.open('resized.bmp').convert('L')

        halftone = ht.halftone(img, ht.square_dot(spacing=1, angle=35))
        halftone.save(self.output_name + '.bmp')
        return self.output_name + '.bmp'

    def convert_to_matrix(self):
        self.image = Image.open(self.output_name + '.bmp')
        self.image_array = self.image.getdata()
        for y_pixel in range(self.image.height):
            self.image_matrix.append([])
            for x_pixel in range(self.image.width):
                self.image_matrix[y_pixel].append(self.image_array[y_pixel * self.image.width + x_pixel])

    def print_text(self):
        self.create_halftone()
        self.convert_to_matrix()
        string_list = []
        for x in self.image_matrix:
            string = ""
            for y in x:
                if y == 255:
                    string += "■"
                else:
                    string += " "
            string_list.append(string)

        for string in string_list:
            print(string)



if __name__ == "__main__":
    from sys import exit
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    from tkinter.simpledialog import askstring
    Tk().withdraw()
    file = askopenfilename(title="Open your file")
    if not file:
        exit(0)
    else:
        ASCIIArt(file).print_text()
        input("press Enter to exit")



