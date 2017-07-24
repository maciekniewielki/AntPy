import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from tkinter.colorchooser import *


class ClassicAnt:

    def __init__(self, size, left_turn=(0, 1)):
        self.board = np.full((size, size), 0, dtype=np.uint8)   # 0- first color
        self.board_size = size
        self.direction = 0                                  # 0,1,2,3- right,up,left,down
        self.position = [size//2]*2
        self.iteration = 0
        self.left_turn = left_turn
        self.number_of_colors = len(left_turn)

    def make_move(self):
        self.iteration += 1

        if self.left_turn[self.board[self.position[0], self.position[1]]]:
            self.direction = (self.direction+1) % 4
        else:
            self.direction = (self.direction-1) % 4

        # print(self.board[self.position[0], self.position[1]])
        self.board[self.position[0], self.position[1]] = (self.board[self.position[0], self.position[1]]+1) % self.number_of_colors
        # print(self.board[self.position[0], self.position[1]])
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
            new_board = np.full((new_size, new_size), False, dtype=np.uint8)
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

        self.directions = [0, 1]
        self._colors = []
        self.color_buttons = []
        self.repeat_step = tk.IntVar()
        self.repeat_delay = tk.IntVar()
        self.number_of_colors = 2

        self.colors = [(255, 255, 255), (0, 0, 0)]
        self.ant = ClassicAnt(1)
        self.current_image = tk.PhotoImage(translate_array_to_image(self.ant.board, self.colors))
        self.title("Langton's Ant")
        self.geometry("800x600")

        self.image_label = tk.Label(text="Board", compound="top")
        self.options_frame = tk.Frame(self, borderwidth=1)
        self.top_options_frame = tk.Frame(self.options_frame, borderwidth=1)
        self.bottom_options_frame = tk.Frame(self.options_frame, relief=tk.RAISED, borderwidth=1)

        self.single_step_button = tk.Button(self.bottom_options_frame, text="Single step", command=self.single_step, font=("Courier", 44))
        self.multi_step_button = tk.Button(self.bottom_options_frame, text="Multi step", command=self.multi_step, font=("Courier", 44))
        self.step_number = tk.Entry(self.bottom_options_frame, width=7, font=("Courier", 44), justify=tk.CENTER)
        self.repeat_checkbox = tk.Checkbutton(self.bottom_options_frame, variable=self.repeat_step, command=self.continuous_step, text="Step continuously?")
        self.reset_button = tk.Button(self.bottom_options_frame, text="Reset", command=self.reset, font=("Courier", 44))
        self.repeat_delay_slider = tk.Scale(self.bottom_options_frame, from_=50, to=1000, orient=tk.HORIZONTAL, variable=self.repeat_delay)

        self.color_label = tk.Label(self.top_options_frame, text="Number of colors", font=("Courier", 44))
        self.color_number_entry = tk.Entry(self.top_options_frame, width=1, font=("Courier", 44), justify=tk.CENTER)

        self.bottom_options_frame.columnconfigure(0, pad=3)
        self.bottom_options_frame.columnconfigure(1, pad=3)
        self.bottom_options_frame.columnconfigure(2, pad=3)
        self.bottom_options_frame.columnconfigure(3, pad=3)
        self.bottom_options_frame.columnconfigure(4, pad=3)

        self.bottom_options_frame.rowconfigure(0, pad=3)
        self.bottom_options_frame.rowconfigure(1, pad=3)
        self.bottom_options_frame.rowconfigure(2, pad=3)
        self.bottom_options_frame.rowconfigure(3, pad=3)

        self.top_options_frame.columnconfigure(0, pad=30)
        self.top_options_frame.columnconfigure(1, pad=30)
        self.top_options_frame.columnconfigure(2, pad=3)

        self.top_options_frame.rowconfigure(0, pad=20)
        self.top_options_frame.rowconfigure(1, pad=3)

        self.options_frame.pack(side="left", expand=True)
        self.bottom_options_frame.pack(side="bottom")
        self.top_options_frame.pack(side="top")
        self.image_label.pack(side="left", expand=True, padx=8, pady=8)

        self.single_step_button.grid(row=0, column=0, columnspan=4)
        self.multi_step_button.grid(row=1, column=0)
        self.step_number.grid(row=1, column=1)
        self.repeat_checkbox.grid(row=2, column=0)
        self.repeat_delay_slider.grid(row=2, column=1, columnspan=4)
        self.reset_button.grid(row=3, columnspan=5)
        self.update_image()

        self.color_label.grid(row=0, column=0, columnspan=1)
        self.color_number_entry.grid(row=0, column=2)

        self.color_number_entry.bind("<Return>", lambda x: self.recreate_color_options())

    def single_step(self):
        self.ant.make_move()
        self.update_image()

    def multi_step(self):
        for x in range(int(self.step_number.get())):
            self.ant.make_move()
        self.update_image()

    def update_image(self):
        self.current_image = ImageTk.PhotoImage(translate_array_to_image(self.ant.board, self.colors).resize((900, 900)))
        self.image_label.configure(image=self.current_image, text="Iteration {0}\nimage size = {1}x{1}".format(self.ant.iteration, self.ant.board_size))

    def continuous_step(self):
        if not self.repeat_step.get():
            return

        self.single_step()
        self.after(self.repeat_delay.get(), self.continuous_step)

    def recreate_color_options(self):
        print("Recreating")

        for child in self.top_options_frame.winfo_children():
            if child != self.color_label and child != self.color_number_entry:
                child.destroy()

        number_of_colors = int(self.color_number_entry.get())
        self.number_of_colors = number_of_colors
        self.directions = [tk.IntVar() for x in range(number_of_colors)]
        self._colors = ["white" for x in range(number_of_colors)]
        self.colors = [(0, 0, 0)] * self.number_of_colors
        self.color_buttons = []

        for num in range(number_of_colors):
            self.top_options_frame.rowconfigure(1+num, pad=3)
            label = tk.Label(self.top_options_frame, text="Color #%d" % (num+1), font=("Courier", 20))
            action = tk.Checkbutton(self.top_options_frame, variable=self.directions[num])
            color = tk.Button(self.top_options_frame, width=5, height=2, name=str(num))

            color.configure(command=lambda x=num: self.set_color(x))
            label.grid(row=num+1, column=0)
            action.grid(row=num+1, column=1)
            color.grid(row=num+1, column=2)

            self.color_buttons.append(color)
        self.reset()

    def set_color(self, button_number):
        color = askcolor()
        self.color_buttons[button_number].configure(bg=color[1])
        self._colors[button_number] = color[1]
        self.colors[button_number] = tuple(int(x) for x in color[0])
        print("Set color number %d to %s" % (button_number, self.colors[button_number]))

    def reset(self):
        self.ant = ClassicAnt(1, [x.get() for x in self.directions])
        self.current_image = tk.PhotoImage(translate_array_to_image(self.ant.board, self.colors))


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

