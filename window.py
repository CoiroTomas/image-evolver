from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
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
    def __init__(self, root):
        self.pool_size = None
        self.generation_survivers = None
        self.original_image = None
        self.iteration = None
        self.image_evolver = None
        self.playing = False
        
        self.oi_image = None
        self.ci_image = None
        self.i100_image = None
        self.i1000_image = None
        self.i2000_image = None
        self.i5000_image = None

        self.root = root
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
        image_entry = ttk.Label(mainframe, width=25, textvariable=self.original_image)
        image_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Button(mainframe, text="Search Image", command=self.open_file).grid(column=2, row=0, sticky=W)

        self.iteration = StringVar()
        ttk.Label(mainframe, text="Iteration:").grid(column=0, row=5, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.iteration).grid(column=0, row=6, sticky=(W, E))

        ttk.Button(mainframe, text="Step", command=self.step).grid(column=2, row=5, sticky=W)
        ttk.Button(mainframe, text="Start New", command=self.start).grid(column=3, row=5, sticky=W)
        ttk.Button(mainframe, text="Stop", command=self.stop).grid(column=5, row=5, sticky=W)
        ttk.Button(mainframe, text="Play", command=self.continue_g).grid(column=4, row=5, sticky=W)

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

        ttk.Button(mainframe, text="Save Current", command=self.save_current).grid(column=1, row=4, sticky=W)
        ttk.Button(mainframe, text="Save Iteration 100", command=self.save_100).grid(column=2, row=4, sticky=W)
        ttk.Button(mainframe, text="Save Iteration 1000", command=self.save_1000).grid(column=3, row=4, sticky=W)
        ttk.Button(mainframe, text="Save Iteration 2000", command=self.save_2000).grid(column=4, row=4, sticky=W)
        ttk.Button(mainframe, text="Save Iteration 5000", command=self.save_5000).grid(column=5, row=4, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        pool_size_entry.focus()
        root.bind("<Return>", self.start)

    def start(self, *args):
        if (self.original_image.get() == ""
            or self.generation_survivers.get() == ""
            or self.pool_size.get() == ""):
            messagebox.Message(parent=self.root, message="Arguments missing").show()
            return
        original_image = None
        try:
            original_image = Image.open(self.original_image.get())
        except:
            messagebox.Message(parent=self.root, message="Error opening image").show()
            return
        self.image_evolver = ImageEvolver(original_image,
                                          int(self.pool_size.get()),
                                          int(self.generation_survivers.get()))
        #self.image_evolver.debug = True #For printing of diff values
        self.iteration.set(0)
        self.playing = False
        self.oi_image = ImageTk.PhotoImage(original_image)
        self.oi_label['image'] = self.oi_image
        self.ci_image = None
        self.i100_image = None
        self.i1000_image = None
        self.i2000_image = None
        self.i5000_image = None
        self.continue_g()

    def continue_g(self, *args):
        self.playing = True

    def stop(self, *args):
        self.playing = False

    def step(self, *args):
        if not self.image_evolver:
            messagebox.Message(self.root, message="Can't advance iterations").show()
            self.playing = False
            return
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
    
    def open_file(self, *args):
        self.original_image.set(
            askopenfilename(initialdir="./",
                            title="Search Image",
                            filetypes=(("JPG", ".jpg"), ("PNG", ".png"))))
    
    def save_current(self, *args):
        img = self.ci_image
        path = "./" + self.iteration.get() + ".png"
        if img:
            ImageTk.getimage(img).save(path)

    def save_1000(self, *args):
        img = self.i1000_image
        path = "./1000.png"
        if img:
            ImageTk.getimage(img).save(path)
            
    def save_100(self, *args):
        img = self.i100_image
        path = "./100.png"
        if img:
            ImageTk.getimage(img).save(path)
    
    def save_2000(self, *args):
        img = self.i2000_image
        path = "./2000.png"
        if img:
            ImageTk.getimage(img).save(path)
    
    def save_5000(self, *args):
        img = self.i5000_image
        path = "./5000.png"
        if img:
            ImageTk.getimage(img).save(path)

t= threading.Thread(target=play_loop)
t.daemon = True
t.start()

root = Tk()
imw = ImageEvolverWindow(root)
root.mainloop()
