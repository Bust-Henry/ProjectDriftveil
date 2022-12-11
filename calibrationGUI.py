import tkinter as tk
from PIL import ImageTk
lvl = None
no = None
stats = None
class GUI(tk.Tk):
    drawn = 0
    def __init__(self, image):
        super().__init__()
        self.withdraw()
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both",expand=True)
        self.image = ImageTk.PhotoImage(image)
        self.photo = self.canvas.create_image(0,0,image=self.image,anchor="nw")

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,"<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.photo,"<B1-Motion>", self.on_move_press)
        self.canvas.tag_bind(self.photo,"<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        global lvl,stats,no
        bbox = self.canvas.bbox(self.rect)
        self.drawn += 1
        if(self.drawn == 1):
            no = bbox
        if(self.drawn == 2):
            lvl = bbox
        if(self.drawn >= 3):
            stats = bbox
            self.withdraw()
            self.canvas.destroy()
            self.quit()

def run(img):
    root = GUI(img)
    root.mainloop()
    global lvl, stats, no
    return no, lvl, stats
    