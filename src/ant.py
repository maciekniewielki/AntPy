import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class ClassicAnt:

    def __init__(self, size):
        self.board = np.full((size, size), False, dtype=bool)  # True=white
        self.board_size = size
        self.direction = 0                                  # 0,1,2,3- right,up,left,down
        self.position = [size//2]*2
        self.iteration = 0

    def make_move(self):
        self.iteration += 1

        if not self.board[self.position[0], self.position[1]]:
            self.direction = (self.direction+1) % 4
        else:
            self.direction = (self.direction-1) % 4

        self.board[self.position[0], self.position[1]] = not self.board[self.position[0], self.position[1]]

        if self.direction == 0:
            self.position[0] += 1
        elif self.direction == 1:
            self.position[1] -= 1
        elif self.direction == 2:
            self.position[0] -= 1
        elif self.direction == 3:
            self.position[1] += 1

        if not ((0 <= self.position[0] < self.board_size) and (0 <= self.position[1] < self.board_size)):
            new_size = self.board_size*2+1
            new_board = np.full((new_size, new_size), False, dtype=bool)
            center = new_size/2
            lower_b = center-self.board_size/2
            upper_b = center+self.board_size/2
            new_board[lower_b:upper_b, lower_b:upper_b] = self.board

            translate_val = (new_size - self.board_size)/2

            self.board = new_board
            self.board_size = new_size
            self.position = [self.position[0]+translate_val, self.position[1]+translate_val]


class AntGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.image_label = tk.Label(text="Board", compound="top")
        self.image_label.pack(side="top", expand=True, padx=8, pady=8)

        self.colors = [(255, 255, 255), (255, 0, 0)]
        self.ant = ClassicAnt(1)
        self.current_image = tk.PhotoImage(translate_array_to_image(self.ant.board, self.colors))
        self.title("Langton's Ant")
        self.geometry("800x600")

        self.single_step_button = tk.Button(text="Single step", command=self.single_step)
        self.multi_step_button = tk.Button(text="Multi step", command=self.multi_step)
        self.step_number = tk.Entry(text="Number of steps")
        self.reset_button = tk.Button(text="Reset", command=lambda: reset(self))
        # self.anim_speed_button = tk.Scale(self.root, from_=1000, to=10000, label="Animation duration(ms)")

        self.single_step_button.pack(side="left")
        self.multi_step_button.pack(side="left")
        self.step_number.pack(side="left")
        self.reset_button.pack(side="left")
        self.update_image()

    def single_step(self):
        self.ant.make_move()
        self.update_image()

    def multi_step(self):
        for x in range(int(self.step_number.get())):
            self.ant.make_move()
        self.update_image()

    def update_image(self):
        self.current_image = ImageTk.PhotoImage(translate_array_to_image(self.ant.board, self.colors).resize((900, 900)))
        self.image_label.configure(image=self.current_image, text="Iteration %d" % self.ant.iteration)


def translate_array_to_image(array, colors):
    rgb_type = np.dtype([('r', np.uint8), ('g', np.uint8), ('b', np.uint8)])
    width, height = array.shape
    copy = np.zeros(width*height, dtype=rgb_type)
    for index, color in enumerate(colors):
        copy[array.flatten() == index] = color
    image = Image.new("RGB", array.shape)
    image.putdata([tuple(x) for x in copy])
    return image


def reset(what):
    what.destroy()
    new_app = AntGUI()
    new_app.mainloop()


if __name__ == "__main__":
    app = AntGUI()
    app.mainloop()

