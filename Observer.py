class Observer:
    def __init__(self, parent):
        self.parent = parent

    def change_logo(self, logo):
        self.parent.change_logo(logo)

    def change_images(self, images):
        self.parent.change_images(images)

    def change_dir(self, directory):
        self.parent.change_dir(directory)

    def remove_image(self, image):
        self.parent.remove_image(image)

    def draw_images(self):
        self.parent.draw()
