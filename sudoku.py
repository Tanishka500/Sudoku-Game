import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_board()
        self.generate_puzzle()
        self.window.mainloop()

    def create_board(self):
        canvas = tk.Canvas(self.window, width=450, height=450)
        canvas.grid(row=0, column=0, columnspan=9)

        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            canvas.create_line(5 + i * 50, 5, 5 + i * 50, 455, width=width, fill="black")
            canvas.create_line(5, 5 + i * 50, 455, 5 + i * 50, width=width, fill="black")

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.window, width=2, font=('Arial', 18), justify='center')
                entry.place(x=5 + j * 50 + 10, y=5 + i * 50 + 10, width=30, height=30)
                self.entries[i][j] = entry

        button_style = {"bg": "light blue", "font": ('Arial', 12, 'bold'), "width": 10}

        solve_button = tk.Button(self.window, text="Solve", command=self.solve, **button_style)
        solve_button.grid(row=1, column=0, columnspan=4, sticky='e', padx=5, pady=5)

        reset_button = tk.Button(self.window, text="Reset", command=self.reset, **button_style)
        reset_button.grid(row=1, column=5, columnspan=4, sticky='w', padx=5, pady=5)

    def generate_puzzle(self):
        self.grid = self.generate_complete_grid()
        self.remove_numbers_from_grid()

        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')
                self.entries[i][j].delete(0, tk.END)
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, self.grid[i][j])
                    self.entries[i][j].config(state='disabled')

    def generate_complete_grid(self):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku_helper(grid)
        return grid

    def remove_numbers_from_grid(self, num_remove=40):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for _ in range(num_remove):
            row, col = cells.pop()
            self.grid[row][col] = 0

    def solve(self):
        self.read_entries()
        if self.solve_sudoku():
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, self.grid[i][j])
        else:
            messagebox.showerror("Error", "No solution exists for the given puzzle.")

    def reset(self):
        self.generate_puzzle()

    def is_valid(self, grid, num, row, col):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True

    def solve_sudoku_helper(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, num, i, j):
                            grid[i][j] = num
                            if self.solve_sudoku_helper(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def solve_sudoku(self):
        self.read_entries()
        if self.solve_sudoku_helper(self.grid):
            return True
        return False

    def read_entries(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get():
                    self.grid[i][j] = int(self.entries[i][j].get())
                else:
                    self.grid[i][j] = 0

if __name__ == "__main__":
    SudokuGame()
