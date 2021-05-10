from PIL import Image
import cv2
import numpy as np
from Gui import Gui
from Observer import Observer
import threading


class App:
    def __init__(self):
        self.images = []
        self.logo = None
        self.directory = None
        self.logo_size = None
        self.errors = []
        self.observer = Observer(self)
        self.gui = Gui(self.observer)
        self.gui.create_gui()

    def get_logo_size(self):
        if self.logo is None:
            return None
        else:
            logo = Image.open(self.logo)
            self.logo_size = logo.size
            return self.logo_size

    def find_position(self, image_path, step=20, margin=10):
        image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 1)
        row = np.full(self.logo_size[1] + margin, 255)
        matrix = np.full((self.logo_size[0] + margin, self.logo_size[1] + margin), 255)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, gray = cv2.threshold(gray, 200, 255, 0)
        gray = cv2.bitwise_not(gray)
        for x in range(0, gray.shape[1] - self.logo_size[1] + 1, step):
            for y in range(0, gray.shape[0] - self.logo_size[0] + 1, step):
                if np.array_equal(row, gray[y, x:self.logo_size[1] + x + margin]):
                    if np.array_equal(matrix, gray[y:self.logo_size[0] + y + margin, x:self.logo_size[1] + x + margin]):
                        return int(x + margin/2), int(y + margin/2)

    def draw(self):
        self.gui.toggle_buttons(disable=True)
        threading.Thread(target=self.draw_images).start()

    def draw_image(self, image_path):
        position = self.find_position(image_path)
        if position is None:
            self.errors.append(image_path)
            return None
        image = Image.open(image_path)
        logo = Image.open(self.logo)
        image_copy = image.copy()
        image_copy.paste(logo, position, logo)
        name = '{}/{}'.format(self.directory, image_path.split('/')[-1])
        if name == image_path:
            name = name.split('/')
            name[-1] = 'new_' + name[-1]
            name = ''.join(name)
        image_copy.save(name)
        return True

    def draw_images(self):
        self.errors = []
        if self.logo is None or self.directory is None:
            self.gui.toggle_buttons(disable=False)
            return
        elif self.logo_size is None:
            self.get_logo_size()
        images = self.images.copy()
        import time
        start = time.time()
        for image in images:
            self.draw_image(image)
            self.images.remove(image)
            self.gui.update_progressbar((len(images) - len(self.images)) / len(images) * 100)
        self.gui.update_progressbar(0)
        self.gui.remove_images()
        self.change_images(self.errors)
        self.gui.toggle_buttons(disable=False)
        print(time.time() - start)

    def change_logo(self, logo):
        self.logo = logo
        self.gui.change_logo_text(logo)

    def change_dir(self, directory):
        self.directory = directory
        self.gui.change_dir_text(directory)

    def change_images(self, images):
        self.images = list(images)
        for image in self.images:
            self.gui.create_image(image)

    def remove_image(self, image):
        self.images.remove(image)
        self.gui.remove_img(image)

    @staticmethod
    def check_value(value, border):
        if value < 0:
            return 0
        elif value > border:
            return border
        else:
            return value


if __name__ == '__main__':
    App()
