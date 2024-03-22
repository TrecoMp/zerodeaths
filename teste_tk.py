import tkinter as tk
from tkinter import ttk

class LargeCombobox(tk.Frame):
    def __init__(self, master, items, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.selected_item = tk.StringVar(master)
        self.combobox = ttk.Combobox(self, textvariable=self.selected_item, values=items, state="readonly", height=10)
        self.combobox.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")

    # Criando uma lista com 90 itens
    items = [f"Item {i}" for i in range(1, 91)]

    large_combobox = LargeCombobox(root, items)
    large_combobox.pack(fill="both", expand=True)

    root.mainloop()
