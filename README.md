# Insert-Watermark
Insert-Watermark is application for inserting watermark to multiple photos.
## Object detection
Object detection works properly only on white background images. Position of watermark is based on detected object, if background isn't white watermark should be inserted in left-bottom corner. 
## Technologies
[opencv-python](https://github.com/opencv/opencv-python)

[Pillow](https://github.com/python-pillow/Pillow)

[numpy](https://github.com/numpy/numpy)
## Setup
Clone this repo to your desktop, go to root directory and run ```pip install -r requirements.txt``` to install all dependencies.
## Usage
After you clone this repo to your desktop and install all dependencies, you can run ```App.py``` in terminal to start the application.
### Buttons
Logo - select watermark

Folder - select output directory

Zdjęcia - select photos

Start - run watermark insertion