from PIL import Image
from Gui import Gui
from Observer import Observer
from logo_scripts import draw_image
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

    def draw(self):
        self.gui.toggle_buttons(disable=True)
        threading.Thread(target=self.draw_images).start()

    def draw_images(self):
        if self.logo is None or self.directory is None or len(self.images) == 0:
            self.gui.toggle_buttons(disable=False)
            return
        logo = Image.open(self.logo)
        images_copy = self.images.copy()
        for image in images_copy:
            result = draw_image(image, logo, 'A', 10, 20)
            if result:
                name = '{}/{}'.format(self.directory, image.split('/')[-1])
                if name == image:
                    name = name.split('/')
                    name[-1] = 'new_' + name[-1]
                    name = ''.join(name)
                result.save(name)
            else:
                self.errors.append(image)
            self.gui.update_progressbar((len(images_copy) - len(self.images)) / len(images_copy) * 100)
            self.images.remove(image)
        self.gui.update_progressbar(0)
        self.gui.remove_images()
        self.change_images(self.errors)
        self.gui.toggle_buttons(disable=False)

    def change_logo(self, logo):
        print(logo)
        self.logo = logo
        self.gui.change_logo_text(logo)

    def change_dir(self, directory):
        self.directory = directory
        self.gui.change_dir_text(directory)

    def change_images(self, images):
        print(images)
        self.images = list(images)
        for image in self.images:
            self.gui.create_image(image)

    def remove_image(self, image):
        self.images.remove(image)
        self.gui.remove_img(image)


if __name__ == '__main__':
    App()
