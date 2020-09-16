# -*- coding: UTF-8 -*-
# use python3.8
# pip install Pillow
# pip install opencv-python

from tkinter import *
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2

# create window
window = Tk()
# set window title
window.title('AIP 60947017S')
# set window size
window.geometry('1100x600')
# set window background color
window.configure(background='#3E4149')
# set window resize false
window.resizable(width=False, height=False)

# initialize two panel
panel_Left = None
panel_Right = None

# upload image
def upload():
    # declare two panel
    global panel_Left
    global panel_Right
    # ask open file
    filename = filedialog.askopenfilename()
    # if file is exist
    if len(filename) > 0:
        # opencv read image and convert from BGR to RGBA
        image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGBA)
        # resize image
        image = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
        # convert image to PIL format
        image = PIL.Image.fromarray(image)
        # convert image to ImageTk format
        image = PIL.ImageTk.PhotoImage(image)
        # if one or more panel none
        if panel_Left == None and panel_Right == None:
            # set image in Left panel
            panel_Left = Label(image=image)
            panel_Left.image = image
            panel_Left.pack(side="left", padx=10, pady=10)
            
            # set image in Right panel
            panel_Right = Label(image=image)
            panel_Right.image = image
            panel_Right.pack(side="right", padx=10, pady=10)
        else:
            print("123")
            # set image in two panel
            panel_Left.configure(image=image)
            panel_Right.configure(image=image)
            panel_Left.image = image
            panel_Right.image = image

# main
def main():
    # create button (window, text, background color, call function)
    button = Button(window, text="上傳圖片", highlightbackground='#3E4149', command=upload)
    # position
    button.pack(side=TOP)
    # run window
    window.mainloop()


# run main function
if __name__ == '__main__':
    main()
