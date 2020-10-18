# -*- coding: UTF-8 -*-
# use python3
# pip install numpy
# pip install Pillow
# pip install opencv-python
# pip install matplotlib==3.1.3

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
        self.button_histogram = None
        self.button_gaussianNoise = None
        self.button_waveletTrans = None
    
    # image to 1D array
    def imageToArray(self, image):
        return image.flatten()
    
    # 1D array to image
    def arrayToImage(self, array):
        return np.reshape(np.array(array), (self.size[0], self.size[1], -1))

    # set Left Image
    def setLeftImage(self, image, event):
        # set image for download
        self.image_Left = image
        # convert color then resize image
        if event != "AlreadyGray":
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
        if event != "GaussianNoise" and event != "Wavelet":
            image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA if event != "Histogram" else cv2.COLOR_BGR2GRAY), 480, 480)
        elif event == "Wavelet":
            image = self.resize(image, 480, 480)
        # if user want see histogram
        if event == "Histogram" or event == "GaussianNoise":
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
            if event == "Original":
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
            # set button normal
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
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
        # set button disabled
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        # set left image
        self.setLeftImage(self.image_Left, "Gray")
        # set right image
        self.setRightImage(self.image_Right, "Histogram")
    
    # set gaussian noise standard deviation
    def setGaussianNoiseSD(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        # create object
        dialog = Dialog(window, '請輸入標準差')
        # wait window
        window.wait_window(dialog.top)
        # if answer is not none
        if dialog.ans != "" and dialog.ans.isdigit():
            self.gaussianNoise(int(dialog.ans))
        # if user click close button
        elif dialog.ans == "close":
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")

    # gaussian noise
    def gaussianNoise(self, SD):
        # set button disabled or normal
        self.button_choise['state'] = NORMAL
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
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
        # set left image
        self.setLeftImage(newimg, "AlreadyGray")
        # set right image
        self.setRightImage(newimg, "GaussianNoise")
    
    # set wavelet transform level
    def setWaveletLevel(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        # create object
        dialog = Dialog(window, '請輸入小波轉換層數 (介於 1~3 之間)')
        # wait window
        window.wait_window(dialog.top)
        # if answer is not none
        if dialog.ans != "" and dialog.ans.isdigit():
            # set left image
            self.setLeftImage(self.image_Left, "Gray")
            # set right image
            self.setRightImage(self.haarFWT(3), "Wavelet")
            # set button normal
            self.button_choise['state'] = NORMAL
        # if user click close button
        elif dialog.ans == "close":
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")
    
    # def haarFWT(self):
    #     img = self.image_Left
    #     image = img.astype(np.float)
    #     height, width = image.shape[:2]
    #     result = np.zeros((height, width, 3), np.float)
    #     width2 = width // 2
    #     for i in range(height):
    #         for j in range(0, width - 1, 2):
    #             j1 = j + 1
    #             j2 = j // 2
    #             result[i, j2] = (image[i, j] + image[i, j1]) // 2
    #             result[i, width2 + j2] = (image[i, j] - image[i, j1]) // 2
    #     image = np.copy(result)
    #     height2 = height // 2
    #     for i in range(0, height - 1, 2):
    #         for j in range(0, width):
    #             i1 = i + 1
    #             i2 = i // 2
    #             result[i2, j] = (image[i, j] + image[i1, j]) // 2
    #             result[height2 + i2, j] = (image[i, j] - image[i1, j]) // 2
    #     resultimg = result.astype(np.uint8)
    #     return resultimg

    def haarFWT(self, level):
        image = self.convertColor(self.image_Left, cv2.COLOR_BGR2GRAY)
        signal = self.imageToArray(image)
        s = .5
        h = [ 1,  1 ]
        g = [ 1, -1 ]
        f = len ( h )
        t = signal
        l = len ( t )
        y = [0] * l
        t = np.pad(array=t, pad_width=(1,1), mode='constant', constant_values=0)
        for i in range ( level ):
            y [ 0:l ] = [0] * l
            l2 = l // 2
            for j in range ( l2 ):
                for k in range ( f ):
                    y [j]    += int(t [ 2*j + k ] * h [ k ] * s)
                    y [j+l2] += int(t [ 2*j + k ] * g [ k ] * s)
            l = l2
            t [ 0:l ] = y [ 0:l ] 
        resultimg = self.arrayToImage(y).astype(image.dtype)
        return resultimg

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
    # create button (frame, text, background color, call function, state)
    imgProcessing.button_choise = Button(frame_button, text="選擇影像", highlightbackground='#051636', command=imgProcessing.upload)
    imgProcessing.button_histogram = Button(frame_button, text="直方圖", highlightbackground='#051636', command=imgProcessing.histogram, state="disabled")
    imgProcessing.button_gaussianNoise = Button(frame_button, text="高斯雜訊", highlightbackground='#051636', command=imgProcessing.setGaussianNoiseSD, state="disabled")
    imgProcessing.button_waveletTrans = Button(frame_button, text="小波轉換", highlightbackground='#051636', command=imgProcessing.setWaveletLevel, state="disabled")
    # position
    imgProcessing.button_choise.grid(row=1, column=1, pady=20, padx=5)
    imgProcessing.button_histogram.grid(row=1, column=2, pady=20, padx=5)
    imgProcessing.button_gaussianNoise.grid(row=1, column=3, pady=20, padx=5)
    imgProcessing.button_waveletTrans.grid(row=1, column=4, pady=20, padx=5)
    # set Text
    text_before = Label(frame_Text, text = "輸入影像", bg="#051636", fg="green")
    text_before.grid(row=1, column=1, padx=195, pady=10)
    text_before.config(font=("Courier", 18)) 

    text_after = Label(frame_Text, text = "輸出影像", bg="#051636", fg="red")
    text_after.grid(row=1, column=2, padx=280, pady=10)
    text_after.config(font=("Courier", 18))
    # run window
    window.mainloop()


# run main function
if __name__ == '__main__':
    main()