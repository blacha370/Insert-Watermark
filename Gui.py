from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
from Observer import Observer


class Gui:
    def __init__(self, observer: Observer):
        self.observer = observer
        self.root = Tk()
        self.mainframe = Frame(master=self.root)
        self.labels_frame = Frame(self.mainframe)
        self.logo_label = Label(self.labels_frame, text='')
        self.logo_text = Label(self.labels_frame, text='Logo: ')
        self.dir_label = Label(self.labels_frame, text='')
        self.dir_text = Label(self.labels_frame, text='Folder: ')
        self.imgs_frame = Frame(self.labels_frame, borderwidth=2, relief="groove")
        self.canvas = Canvas(self.imgs_frame, width=700)
        self.scrollbar = Scrollbar(self.imgs_frame, orient='vertical', command=self.canvas.yview)
        self.images_frame = Frame(self.canvas)
        self.images_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.images_frame, anchor='nw')
        self.buttons_frame = Frame(self.mainframe)
        self.logo_button = Button(self.buttons_frame, text='Logo', command=self.change_logo)
        self.dir_button = Button(self.buttons_frame, text='Folder', command=self.change_dir)
        self.images_button = Button(self.buttons_frame, text='Zdjęcia', command=self.select_images)
        self.run_button = Button(self.buttons_frame, text='Start', command=self.draw_images)
        self.progressbar = Progressbar(self.mainframe, orient=HORIZONTAL, length=1, mode='determinate')
        self.place_elements()

    def place_elements(self):
        self.mainframe.pack()
        self.mainframe.columnconfigure(0, minsize=300, weight=1)
        self.mainframe.columnconfigure(1, minsize=50, weight=0)
        self.labels_frame.grid(row=0, column=0)
        self.labels_frame.columnconfigure(1, weight=1)
        self.logo_text.grid(row=0, column=0)
        self.logo_label.grid(row=0, column=1)
        self.dir_text.grid(row=1, column=0)
        self.dir_label.grid(row=1, column=1)
        self.imgs_frame.grid(row=2, column=0, columnspan=2)
        self.canvas.pack(side="left", fill="both")
        self.scrollbar.pack(side='right', fill='y')
        self.buttons_frame.grid(row=0, column=1, sticky='N')
        self.logo_button.pack(side='top', fill=BOTH, expand=True)
        self.dir_button.pack(side='top', fill=BOTH, expand=True)
        self.images_button.pack(side='top', fill=BOTH, expand=True)
        self.run_button.pack(side='top', fill=BOTH, expand=True)
        self.progressbar.grid(row=1, column=0, columnspan=2, sticky='EW')

    def change_logo(self):
        logo = askopenfilename(filetypes=[('Logo', '*.png')])
        self.observer.change_logo(logo)

    def change_logo_text(self, text):
        self.logo_label['text'] = text

    def change_dir(self):
        directory = askdirectory()
        self.observer.change_dir(directory)

    def change_dir_text(self, text):
        self.dir_label['text'] = text

    def select_images(self):
        self.remove_images()
        images = askopenfilenames(filetypes=[('Zdjęcie', '*jpg')])
        self.observer.change_images(images)

    def create_image(self, image):
        frame = Frame(self.images_frame)
        frame.pack(fill=BOTH, expand=True)
        label = Label(frame, text=image)
        button = Button(frame, text='Usuń', command=lambda: self.remove_image(image))
        button.pack(side='left')
        label.pack(side='left')

    def remove_image(self, image):
        self.observer.remove_image(image)

    def remove_img(self, image):
        for frame in self.images_frame.slaves():
            if frame.winfo_children()[0]['text'] == image:
                frame.destroy()

    def remove_images(self):
        for frame in self.images_frame.slaves():
            frame.destroy()

    def update_progressbar(self, value):
        self.progressbar['value'] = value
        self.root.update_idletasks()

    def draw_images(self):
        self.observer.draw_images()

    def toggle_buttons(self, disable):
        if disable:
            self.logo_button['state'] = "disabled"
            self.dir_button['state'] = "disabled"
            self.images_button['state'] = "disabled"
            self.run_button['state'] = "disabled"
        else:
            self.logo_button['state'] = "normal"
            self.dir_button['state'] = "normal"
            self.images_button['state'] = "normal"
            self.run_button['state'] = "normal"

    def create_gui(self):
        self.root.mainloop()
