# -*- coding: UTF-8 -*-
# use python3
# pip install Pillow
# pip install opencv-python

from tkinter import *
from tkinter import filedialog, messagebox
import PIL.Image, PIL.ImageTk
import cv2
import os

# initialize window size
width = 1280
height = 600

# create window
window = Tk()
# set window title
window.title('AIP 60947017S')
# set window size
window.geometry('%dx%d+%d+%d' % (width, height, (window.winfo_screenwidth() - width)/2, (window.winfo_screenheight() - height)/2))
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
        image = cv2.resize(image, (480, 480), interpolation=cv2.INTER_CUBIC)
        # convert image to PIL format
        image = PIL.Image.fromarray(image)
        # convert image to ImageTk format
        image = PIL.ImageTk.PhotoImage(image)

        # set Text
        text_before = Label(window, text = "輸入影像", bg="#3E4149", fg="green")
        text_before.pack(side="left", padx=10)
        text_before.config(font =("Courier", 18)) 
        text_after = Label(window, text = "輸出影像", bg="#3E4149", fg="red")
        text_after.pack(side="right", padx=10)
        text_after.config(font =("Courier", 18))
        
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
            # set image in two panel
            panel_Left.configure(image=image)
            panel_Right.configure(image=image)
            panel_Left.image = image
            panel_Right.image = image
        # show messagebox
        messagebox.showinfo( "提醒", "已上傳 " + os.path.splitext(filename)[-1] + " 檔案")

# main
def main():
    # create frame
    frame =Frame(window, background='#3E4149')
    frame.pack()
    # create button (frame, text, background color, call function)
    button_choise = Button(frame, text="選擇影像", highlightbackground='#3E4149', command=upload)
    button_save = Button(frame, text="儲存影像", highlightbackground='#3E4149', command=upload)
    # position
    button_choise.grid(row=1, column=1, pady=20, padx=5)
    button_save.grid(row=1, column=2, pady=20, padx=5)
    # run window
    window.mainloop()


# run main function
if __name__ == '__main__':
    main()
