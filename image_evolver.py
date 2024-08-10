from PIL import Image, ImageDraw
from random import random, choice, shuffle, randrange

img = None
try: 
    img  = Image.open("image.jpg") 
except IOError:
    exit

def sort_func(ic):
    return ic.saved_diff
    
class Shape:
    def __init__(self, width, height):
        self.edit_x(width, height)
        self.edit_y(width, height)
        self.edit_r(width, height)
        self.color = (int(random() * 256),int(random() * 256),
             int(random() * 256))

    def copy(self):
        new_s = Shape(1, 1)
        new_s.x = self.x
        new_s.y = self.y
        new_s.r = self.r
        new_s.color = self.color
        return new_s

    def edit_random(self, width, height):
        r = random()
        if r < 0.05:
            self.edit_x(width, height)
        elif r < 0.1:
            self.edit_y(width, height)
        elif r < 0.2:
            self.edit_r(width, height)
        else:
            self.edit_random_color()

    def edit_x(self, width, height):
        self.x = int(random() * width)

    def edit_y(self, width, height):
        self.y = int(random() * height)

    def edit_r(self, width, height):
        self.r = int(random() * max(width, height) * 0.3)

    def edit_random_color(self):
        r = random()
        (c1,c2,c3) = self.color
        if r < 0.3:
            self.color = (int(random() * 256),c2,c3)
        elif r < 0.6:
            self.color = (c1,int(random() * 256),c3)
        elif r < 0.9:
            self.color = (c1,c2,int(random() * 256))
        else:
            self.color = (int(random() * 256),int(random() * 256),
             int(random() * 256))

class ImageCreator:
    width = 1
    height = 1
    shapes = []
    saved_diff = 0
    last_generated_image = None

    def init_image(self):
        self.last_generated_image = Image.new("RGB",
                (self.width, self.height), (255, 255, 255))

    def __init__(self, original_image):
        self.width, self.height = original_image.size

    def generate_image(self):
        draw = ImageDraw.Draw(self.last_generated_image)
        draw.rectangle([0,0, self.width, self.height], (255,255,255))

        for s in self.shapes:
            draw.circle((s.x,s.y), s.r, s.color)

    def generate_creator_from_self(self, new_creator):
        new_creator.shapes = self.copy_shapes()
        new_creator.width = self.width
        new_creator.height = self.height
        return new_creator

    def copy_shapes(self):
        shapes = [None] * len(self.shapes)
        for i in range(len(self.shapes)):
            shapes[i] = self.shapes[i].copy()
        return shapes

    def compare_images(self, i2):
        i1 = self.last_generated_image
        pairs = zip(i1.getdata(), i2.getdata())
        self.saved_diff = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        return self.saved_diff

    def change_shapes(self):
        r = random()
        if len(self.shapes) == 0:
            self.add_shape()
            self.add_shape()
            self.add_shape()
            self.add_shape()
        elif r < 0.05:
            self.shapes.pop(randrange(len(self.shapes))) 
        elif r < 0.93:
            self.edit_random_shape()
        elif r < 0.98:
            self.add_shape()
        else:
            shuffle(self.shapes)

    def edit_random_shape(self):
        s = choice(self.shapes)
        s.edit_random(self.width, self.height)

    def add_shape(self):
        self.shapes.append(Shape(self.width, self.height))
    

class ImageEvolver:
    original_image = None
    image_pool = []
    step = 0
    top = 3
    gen = 32

    def __init__(self, original_image, pool_size, generation_survivers):
        self.original_image = original_image
        self.top = generation_survivers
        self.gen = int(pool_size/generation_survivers) - 1
        for i in range(pool_size):
            ic = ImageCreator(original_image)
            ic.init_image()
            ic.change_shapes()
            ic.generate_image()
            ic.compare_images(self.original_image)
            self.image_pool.append(ic)

    def add_shapes_and_compare(self):
        for ic in self.image_pool[3:]:
            ic.change_shapes()
            ic.generate_image()
            ic.compare_images(self.original_image)

    def sort(self):
        self.image_pool.sort(key=sort_func)

    def replicate_pool(self):
        for j in range(self.top):
            ic = self.image_pool[j]
            for i in range(self.gen):
                ic.generate_creator_from_self(self.image_pool[self.top+j*self.gen+i])

    def step(self):
        self.add_shapes_and_compare()
        self.sort()
        self.replicate_pool()
        for i in range(self.top):
            print(str(1+i) + ") " + str(self.image_pool[i].saved_diff))
        return self.image_pool[0].last_generated_image

evolver = ImageEvolver(img, 22, 2)
for i in range(10000):
    print("\n" + str(i+1))
    b = evolver.step()
    if i+1 == 100:
        b.save("100.png")
    elif i+1 == 500:
        b.save("500.png") 
    elif i+1 == 1000:
        b.save("1000.png")
    elif i+1 == 2000:
        b.save("2000.png")
    elif i+1 == 5000:
        b.save("5000.png")
    elif i+1 == 10000:
        b.save("10000.png")
