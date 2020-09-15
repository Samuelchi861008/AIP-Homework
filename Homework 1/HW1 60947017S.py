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
window.geometry('800x600')
# set window background color
window.configure(background='#3E4149')

# upload image
def upload():
    # initialize two panel
    panelA = None
    panelB = None
    # ask open file
    filename = filedialog.askopenfilename()
    # if file is exist
    if len(filename) > 0:
        # opencv read image
        image = cv2.imread(filename)
        # convert image to PIL format
        image = PIL.Image.fromarray(image)
        # convert image to ImageTk format
        image = PIL.ImageTk.PhotoImage(image)
        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=image)
            panelB.image = image
            panelB.pack(side="right", padx=10, pady=10)
        else:
            panelA.configure(image=image)
            panelB.configure(image=image)
            panelA.image = image
            panelB.image = image

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
