# -*- coding: UTF-8 -*-
# use python3
# pip install Pillow
# pip install opencv-python
# pip install matplotlib

import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
        self.image_Left = None
        self.image_Right = None
        self.size = None
        self.canvas = None

    # set Left Image
    def setLeftImage(self, image, event):
        # set image for download
        self.image_Left = image
        # convert color then resize image
        image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA if event != "Gray" else cv2.COLOR_BGR2GRAY), 480, 480)
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
        # if not None clear Right panel
        if self.panel_Right != None:
            self.canvas.get_tk_widget().destroy() if isinstance(self.panel_Right, Figure) else self.panel_Right.destroy()
        # set image for download
        self.image_Right = image
        # convert color then resize image
        image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA if event != "Histogram" else cv2.COLOR_BGR2GRAY), 480, 480)
        # if user want see histogram
        if event == "Histogram":
            # set Right panel is Figure
            self.panel_Right = Figure(figsize=(4.8, 4.8), dpi=100)
            # set Right panel plot
            plot = self.panel_Right.add_subplot(111)
            plot.title.set_text('Image Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            # set canvas
            self.canvas = FigureCanvasTkAgg(self.panel_Right, window)
            # set canvas position
            self.canvas.get_tk_widget().pack(side="right", padx=10, pady=10)
        else:
            # convert image to PIL then convert to ImageTk format
            image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
            # set image in Right panel
            self.panel_Right = Label(image=image)
            self.panel_Right.image = image
            self.panel_Right.pack(side="right", padx=10, pady=10)
            # set panel click event
            self.panel_Right.bind("<Button-1>", self.download)

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

    # download image
    def download(self, event):
        # ask save file name
        saveFileName = filedialog.asksaveasfilename()
        extensionFileName = os.path.splitext(saveFileName)[-1].upper() if (os.path.splitext(saveFileName)[-1]) else ".JPG"
        # if file isn't gif
        if len(saveFileName) > 0 and extensionFileName == ".GIF":
            # show messagebox
            messagebox.showinfo("警告", "不可儲存 .gif 檔")
        elif len(saveFileName) > 0:
            # image write
            cv2.imencode(extensionFileName, self.image_Right)[1].tofile(saveFileName if (os.path.splitext(saveFileName)[-1]) else (saveFileName + extensionFileName))
            # show messagebox
            messagebox.showinfo("提醒", "已下載 " + extensionFileName + " 檔案\n大小為 " + str(cv2.imdecode(np.fromfile(saveFileName if (os.path.splitext(saveFileName)[-1]) else (saveFileName + extensionFileName), dtype=np.uint8), 1).shape[0:2]))
    
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

    # draw histogram
    def histogram(self):
        self.setLeftImage(self.image_Left, "Gray")
        self.setRightImage(self.image_Right, "Histogram")

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
    button_histogram = Button(frame_button, text="直方圖", highlightbackground='#051636', command=imgProcessing.histogram)
    # position
    button_choise.grid(row=1, column=1, pady=20, padx=5)
    button_histogram.grid(row=1, column=2, pady=20, padx=5)
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