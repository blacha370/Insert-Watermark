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

    def find_position(self, image_path):
        try:
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 1)
            cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), (255, 255, 255), 10)
            logo_area = (self.logo_size[0] + 10) * (self.logo_size[1] + 10)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, gray = cv2.threshold(gray, 200, 255, 0)
            gray = cv2.bitwise_not(gray)
            contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) > logo_area:
                    step = 10
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    max_points = np.amax(box, axis=0)
                    min_points = np.min(box, axis=0)
                    center = np.int0((max_points + min_points) / 2)
                    update = {'left': True, 'right': True, 'top': True, 'bottom': True}
                    left = self.check_value(center[0] - 1, image.shape[1])
                    right = self.check_value(center[0] + 1, image.shape[1])
                    top = self.check_value(center[1] - 1, image.shape[0])
                    bottom = self.check_value(center[1] + 1, image.shape[0])
                    while update['left'] or update['right'] or update['top'] or update['bottom']:
                        if update['left']:
                            left = self.check_value(left - step, image.shape[1])
                            if np.where(gray[top:bottom, left:left + step] == 0
                                        )[0].size / gray[top:bottom, left:left + 10].size > 0.01 or left == step:
                                left = self.check_value(left + 10, image.shape[1])
                                update['left'] = False
                        if update['right']:
                            right = self.check_value(right + step, image.shape[1])
                            if np.where(gray[top:bottom, right - step:right] == 0
                                        )[0].size / gray[top:bottom, right - step:right].size > 0.01 or \
                                    right == image.shape[1]:
                                right = self.check_value(right - 10, image.shape[1])
                                update['right'] = False
                        if update['top']:
                            top = self.check_value(top - step, image.shape[0])
                            if np.where(gray[top:top + step, left:right] == 0
                                        )[0].size / gray[top:top + step, left:right].size > 0.01 or top == step:
                                top = self.check_value(top + 10, image.shape[0])
                                update['top'] = False
                        if update['bottom']:
                            bottom = self.check_value(bottom + step, image.shape[0])
                            if np.where(gray[bottom - step:bottom, left:right] == 0
                                        )[0].size / gray[bottom - step:bottom, left:right].size > 0.01 or bottom == image.shape[0]:
                                bottom = self.check_value(bottom - 10, image.shape[0])
                                update['bottom'] = False
                    square = gray[top:bottom, left:right]
                    if square.shape[0] >= self.logo_size[0] + 10 and square.shape[1] >= self.logo_size[1] + 10:
                        return left + 5, bottom - 5 - self.logo_size[0]
        except ValueError:
            return None
        except ZeroDivisionError:
            return None

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
