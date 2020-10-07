# -*- coding: UTF-8 -*-
# use python3
# pip install numpy
# pip install Pillow
# pip install opencv-python

import numpy as np
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

# dialog class
class Dialog:
    # constructor (parent window, question)
    def __init__(self, parent, text):
        # answer
        self.ans = None
        # set dialog width
        self.dialogWidth = 500
        # set dialog height
        self.dialogHeight = 100
        # set dialog
        self.top = Toplevel(parent)
        self.top.protocol("WM_DELETE_WINDOW", self.clickCloseButton)
        self.top.geometry('%dx%d+%d+%d' % (self.dialogWidth, self.dialogHeight, (window.winfo_screenwidth() - self.dialogWidth)/2, (window.winfo_screenheight() - self.dialogHeight)/2))
        self.top.configure(background='#39393a')
        self.top.resizable(width=False, height=False)
        # question label
        self.myLabel = Label(self.top, text=text, fg='#ffffff', bg='#39393a')
        self.myLabel.pack()
        # input box
        self.myEntryBox = Entry(self.top, highlightbackground='#39393a')
        self.myEntryBox.pack(pady=5)
        # submit button
        self.mySubmitButton = Button(self.top, text='確定', command=self.send, highlightbackground='#39393a')
        self.mySubmitButton.pack()
    # when user click submit button
    def send(self): 
        self.ans = self.myEntryBox.get()
        self.top.destroy()
    # when user click close button
    def clickCloseButton(self):
        self.ans = "close"
        self.top.destroy()

# image processing class
class ImgProcessing:
    # constructor
    def __init__(self):
        # data field
        self.panel_Left = None
        self.panel_Right = None
        self.imgPath = None
        self.image_Left = None
        self.image_Right = None
        self.size = None
        self.canvas = None
        self.button_choise = None

    # set Left Image
    def setLeftImage(self, image, event):
        # set image for download
        self.image_Left = image
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
    def setRightImage(self, image, event):
        # set image for download
        self.image_Right = image
        # convert color then resize image
        image = self.resize(self.canny(self.convertColor(image, cv2.COLOR_BGR2GRAY)), 480, 480)
        # convert image to PIL then convert to ImageTk format
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
        # if panel is none
        if self.panel_Right == None:
            # set image in Left panel
            self.panel_Right = Label(image=image)
            self.panel_Right.image = image
            self.panel_Right.pack(side="right", padx=10, pady=10)
        else:
            # set image in panel
            self.panel_Right.configure(image=image)
            self.panel_Right.image = image

    # upload image
    def upload(self):
        # ask open file
        self.imgPath = filedialog.askopenfilename()
        extensionFileName = os.path.splitext(self.imgPath)[-1].upper()
        # if file is exist and not gif
        if len(self.imgPath) > 0 and extensionFileName == ".GIF":
            # show messagebox
            messagebox.showinfo("警告", "不可選擇 .gif 檔")
        elif len(self.imgPath) > 0:
            # image read by openCV
            image = cv2.imdecode(np.fromfile(self.imgPath, dtype=np.uint8), 1)
            # get image size
            self.size = image.shape
            # set two panel image
            self.setLeftImage(image, "Original")
            self.setRightImage(image, "Original")
            # show messagebox
            messagebox.showinfo("提醒", "已上傳 " + extensionFileName + " 檔案\n大小為 " + str(self.size[0:2]))
    
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
    
    # image canny
    def canny(self, image, low_threshold=100, high_threshold=20):
        # opencv canny image
        image = cv2.Canny(image, low_threshold, high_threshold)
        return image
    
    # set gaussian noise standard deviation
    def setGaussianNoiseSD(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        # create object
        dialog = Dialog(window, '請輸入標準差')
        # wait window
        window.wait_window(dialog.top)
        # if answer is not none
        if dialog.ans != "" and dialog.ans.isdigit():
            return self.gaussianNoise(int(dialog.ans))
        # if user click close button
        elif dialog.ans == "close":
            # set button normal
            self.button_choise['state'] = NORMAL
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")

    # gaussian noise
    def gaussianNoise(self, SD):
        # set button disabled or normal
        self.button_choise['state'] = NORMAL
        # range of grayscale
        grayscale = 256
        # initialize a value, if low value generate less noise
        param = SD
        # convert image to gray then resize it
        image = self.resize(self.convertColor(self.image_Left, cv2.COLOR_BGR2GRAY), 480, 480)
        # initialize a array then filled with zero
        newimg = np.zeros((480, 480), np.uint8)
        # use nested loops read image every pixel
        for i in range(0, 480):
            for j in range(0, 480, 2):
                # generate two random number
                r1 = np.random.random_sample()
                r2 = np.random.random_sample()
                # calculate z1 and z2
                z1 = param * np.cos(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                z2 = param * np.sin(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                # calculate f'(x,y) and f'(x,y+1)
                fxy = int(image[i, j] + z1)
                fxy1 = int(image[i, j + 1] + z2)
                # condition for f(x,y)
                if fxy < 0:
                    fxy_val = 0
                elif fxy > grayscale - 1:
                    fxy_val = grayscale - 1
                else:
                    fxy_val = fxy
                # condition for f(x,y+1)
                if fxy1 < 0:
                    fxy1_val = 0
                elif fxy1 > grayscale - 1:
                    fxy1_val = grayscale - 1
                else:
                    fxy1_val = fxy1
                # set two values in new image
                newimg[i, j] = fxy_val
                newimg[i, j + 1] = fxy1_val
        return newimg

# main
def main():
    # create object
    imgProcessing = ImgProcessing()
    # create frame for button
    frame_button = Frame(window, background='#051636')
    frame_button.pack(side=TOP)
    # create button (frame, text, background color, call function, state)
    imgProcessing.button_choise = Button(frame_button, text="選擇影像", highlightbackground='#051636', command=imgProcessing.upload)
    # position
    imgProcessing.button_choise.grid(row=1, column=1, pady=20, padx=5)
    # run window
    window.mainloop()


# run main function
if __name__ == '__main__':
    main()