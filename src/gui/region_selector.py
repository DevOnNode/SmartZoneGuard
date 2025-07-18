import tkinter as tk

class RegionSelector(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.config(bg='gray')
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect = None
        self.canvas = tk.Canvas(self, cursor="cross", bg='gray', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.result = None

    def on_press(self, event):
        self.start_x = self.canvas.winfo_pointerx()
        self.start_y = self.canvas.winfo_pointery()
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_drag(self, event):
        cur_x = self.canvas.winfo_pointerx()
        cur_y = self.canvas.winfo_pointery()
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        self.end_x = self.canvas.winfo_pointerx()
        self.end_y = self.canvas.winfo_pointery()
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        self.result = (x1, y1, x2, y2)
        self.destroy()


def select_region():
    root = tk.Tk()
    root.withdraw()
    selector = RegionSelector(root)
    selector.wait_window()
    root.destroy()
    return selector.result 