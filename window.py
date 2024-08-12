from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from image_evolver import ImageEvolver
import threading
import time

imw = None

def play_loop():
    while True:
        if imw and imw.playing:
            imw.step()
        else:
            time.sleep(1)

class ImageEvolverWindow:
    pool_size = None
    generation_survivers = None
    original_image = None
    iteration = None
    image_evolver = None
    playing = False

    oi_image = None
    ci_image = None
    i100_image = None
    i1000_image = None
    i2000_image = None
    i5000_image = None

    def __init__(self, root):
        root.title("Image Evolver")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.minsize(800, 600)

        self.pool_size = StringVar()
        pool_size_entry = ttk.Entry(mainframe, width=7, textvariable=self.pool_size)
        pool_size_entry.grid(column=1, row=1, sticky=(W, E))

        self.generation_survivers = StringVar()
        generation_survivers_entry = ttk.Entry(mainframe, width=7, textvariable=self.generation_survivers)
        generation_survivers_entry.grid(column=3, row=1, sticky=(W, E))

        self.original_image = StringVar()
        image_entry = ttk.Entry(mainframe, width=25, textvariable=self.original_image)
        image_entry.grid(column=1, row=0, sticky=(W, E))

        self.iteration = StringVar()
        ttk.Label(mainframe, textvariable=self.iteration).grid(column=0, row=5, sticky=(W, E))

        ttk.Button(mainframe, text="Step", command=self.step).grid(column=2, row=4, sticky=W)
        ttk.Button(mainframe, text="Init Generation", command=self.start).grid(column=3, row=4, sticky=W)
        ttk.Button(mainframe, text="Stop Generation", command=self.stop).grid(column=5, row=4, sticky=W)
        ttk.Button(mainframe, text="Play Generation", command=self.continue_g).grid(column=4, row=4, sticky=W)

        ttk.Label(mainframe, text="Original Image").grid(column=0, row=0, sticky=W)
        ttk.Label(mainframe, text="Pool Size").grid(column=0, row=1, sticky=W)
        ttk.Label(mainframe, text="Generation Survivers").grid(column=2, row=1, sticky=E)

        ttk.Label(mainframe, text="Original Image").grid(column=0, row=2, sticky=W)
        ttk.Label(mainframe, text="Current Iteration").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="Iteration 100").grid(column=2, row=2, sticky=W)
        ttk.Label(mainframe, text="Iteration 1000").grid(column=3, row=2, sticky=W)
        ttk.Label(mainframe, text="Iteration 2000").grid(column=4, row=2, sticky=W)
        ttk.Label(mainframe, text="Iteration 5000").grid(column=5, row=2, sticky=W)

        self.oi_label = ttk.Label(mainframe, image=None)
        self.oi_label.grid(column=0, row=3, sticky=W)
        self.ci_label = ttk.Label(mainframe, image=None)
        self.ci_label.grid(column=1, row=3, sticky=W)
        self.i100_label = ttk.Label(mainframe, image=None)
        self.i100_label.grid(column=2, row=3, sticky=W)
        self.i1000_label = ttk.Label(mainframe, image=None)
        self.i1000_label.grid(column=3, row=3, sticky=W)
        self.i2000_label = ttk.Label(mainframe, image=None)
        self.i2000_label.grid(column=4, row=3, sticky=W)
        self.i5000_label = ttk.Label(mainframe, image=None)
        self.i5000_label.grid(column=5, row=3, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        pool_size_entry.focus()
        root.bind("<Return>", self.start)

    def start(self, *args):
        original_image = Image.open("./"+self.original_image.get())
        self.image_evolver = ImageEvolver(original_image,
                                          int(self.pool_size.get()),
                                          int(self.generation_survivers.get()))
        self.iteration.set(0)
        self.playing = False
        self.oi_image = ImageTk.PhotoImage(original_image)
        self.oi_label['image'] = self.oi_image
        self.ci_image = None
        self.i100_image = None
        self.i1000_image = None
        self.i2000_image = None
        self.i5000_image = None

    def continue_g(self, *args):
        self.playing = True

    def stop(self, *args):
        self.playing = False

    def step(self, *args):
        self.iteration.set(int(self.iteration.get()) + 1)
        current_best = ImageTk.PhotoImage(self.image_evolver.step())
        self.ci_image = current_best
        self.ci_label['image'] = current_best
        if int(self.iteration.get()) == 100:
            self.i100_image = current_best
            self.i100_label['image'] = current_best
        if int(self.iteration.get()) == 1000:
            self.i1000_image = current_best
            self.i1000_label['image'] = current_best
        if int(self.iteration.get()) == 2000:
            self.i2000_image = current_best
            self.i2000_label['image'] = current_best
        if int(self.iteration.get()) == 5000:
            self.i5000_image = current_best
            self.i5000_label['image'] = current_best

t= threading.Thread(target=play_loop)
t.daemon = True
t.start()

root = Tk()
imw = ImageEvolverWindow(root)
root.mainloop()
