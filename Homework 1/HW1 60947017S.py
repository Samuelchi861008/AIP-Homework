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
width = 1045
height = 625

# create window
window = Tk()
# set window title
window.title('AIP 60947017S')
# set window size
window.geometry('%dx%d+%d+%d' % (width, height, (window.winfo_screenwidth() - width)/2, (window.winfo_screenheight() - height)/2))
# set window background color
window.configure(background='#051636')
# set window resize false
window.resizable(width=False, height=False)


# image processing class
class ImgProcessing:
    # constructor
    def __init__(self):
        # data field
        self.panel_Left = None
        self.panel_Right = None
        self.imgPath = None
        self.image = None

    # set Left Image
    def setLeftImage(self, image):
        # convert color then resize image
        image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA), 480, 480)
        # convert image to PIL then convert to ImageTk format
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
        # if panel is none
        if self.panel_Left == None:
            # set image in Left panel
            self.panel_Left = Label(image=image)
            self.panel_Left.image = image
            self.panel_Left.pack(side="left", padx=10, pady=10)
        else:
            # set image in panel
            self.panel_Left.configure(image=image)
            self.panel_Left.image = image

    # set Right Image
    def setRightImage(self, image):
        # set image for download
        self.image = image
        # convert color then resize image
        image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA), 480, 480)
        # convert image to PIL then convert to ImageTk format
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
        if self.panel_Right == None:
            # set image in Right panel
            self.panel_Right = Label(image=image)
            self.panel_Right.image = image
            self.panel_Right.pack(side="right", padx=10, pady=10)
        else:
            # set image in two panel
            self.panel_Right.configure(image=image)
            self.panel_Right.image = image
        # set panel click event
        self.panel_Right.bind("<Button-1>", self.download)

    # upload image
    def upload(self):
        # ask open file
        self.imgPath = filedialog.askopenfilename()
        # if file is exist and not gif
        if len(self.imgPath) > 0 and os.path.splitext(self.imgPath)[-1].upper() == ".GIF":
            # show messagebox
            messagebox.showinfo("警告", "不可選擇 .gif 檔")
        elif len(self.imgPath) > 0:
            # image read by openCV
            image = cv2.imread(self.imgPath)
            # set two panel image
            self.setLeftImage(image)
            self.setRightImage(image)
            # show messagebox
            messagebox.showinfo("提醒", "已上傳 " + os.path.splitext(self.imgPath)[-1] + " 檔案")

    # download image
    def download(self, event):
        # ask save file name
        saveFileName = filedialog.asksaveasfilename()
        # if file isn't gif
        if len(saveFileName) > 0 and os.path.splitext(saveFileName)[-1].upper() == ".GIF":
            # show messagebox
            messagebox.showinfo("警告", "不可儲存 .gif 檔")
        elif len(saveFileName) > 0:
            # image write
            cv2.imwrite(saveFileName, self.image)
            # show messagebox
            messagebox.showinfo("提醒", "已下載 " + os.path.splitext(saveFileName)[-1] + " 檔案")
    
    # image resize
    def resize(self, image, width, height):
        # opencv resize image
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
        return image

    # image convert color by openCV
    def convertColor(self, image, event):
        # opencv convert image color
        image = cv2.cvtColor(image, event)
        return image


# main
def main():
    # create object
    imgProcessing = ImgProcessing()
    # create frame for button
    frame_button = Frame(window, background='#051636')
    frame_button.pack(side=TOP)
    # create frame for Text
    frame_Text = Frame(window, background='#051636')
    frame_Text.pack(side=BOTTOM)
    # create button (frame, text, background color, call function)
    button_choise = Button(frame_button, text="選擇影像", highlightbackground='#051636', command=imgProcessing.upload)
    # position
    button_choise.grid(row=1, column=1, pady=20, padx=5)
    # set Text
    text_before = Label(frame_Text, text = "輸入影像", bg="#051636", fg="green")
    text_before.grid(row=1, column=1, padx=200, pady=10)
    text_before.config(font=("Courier", 18)) 

    text_after = Label(frame_Text, text = "輸出影像", bg="#051636", fg="red")
    text_after.grid(row=1, column=2, padx=280, pady=10)
    text_after.config(font=("Courier", 18))
    # run window
    window.mainloop()


# run main function
if __name__ == '__main__':
    main()
