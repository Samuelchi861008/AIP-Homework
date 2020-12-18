# -*- coding: UTF-8 -*-
# use python 3.7.9
# pip install numpy
# pip install Pillow
# pip install opencv-python
# pip install matplotlib==3.1.3

import numpy as np
import pytesseract
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
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
        self.dialogHeight = 110
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
        self.panel_LeftHisEqu = None
        self.panel_RightHisEqu = None
        self.imgPath = None
        self.image_original = None
        self.image_Left = None
        self.image_Right = None
        self.frame_Left = None
        self.frame_Right = None
        self.size = None
        self.canvasLeft = None
        self.canvasRight = None
        self.button_choise = None
        self.button_histogram = None
        self.button_gaussianNoise = None
        self.button_waveletTrans = None
        self.button_histogramEq = None
        self.button_convolution = None
        self.button_canny = None
        self.button_ocr = None
        self.openwindow = None
        self.entry = None

    # set Left Image
    def setLeftImage(self, image, event):
        # set image for download
        self.image_Left = image
        # if not None clear Right panel
        if self.panel_Left != None or self.panel_LeftHisEqu != None:
            self.canvasLeft.get_tk_widget().destroy() if isinstance(self.panel_Left, Figure) else self.panel_Left.destroy()
            if isinstance(self.panel_LeftHisEqu, Figure):
                self.canvasLeft.get_tk_widget().destroy()
                self.frame_Left.destroy()
        # convert color then resize image
        if event != "AlreadyGray" and event != "HistogramEqualization":
            image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA if event != "Gray" else cv2.COLOR_BGR2GRAY), 480, 480)
        if event == "HistogramEqualization":
            # create frame
            self.frame_Left = Frame(window, background='#051636')
            self.frame_Left.pack(side=LEFT)
            # convert image to PIL then convert to ImageTk format
            PILImage = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.resize(image, 480, 240)))
            # set image in Right panel top
            self.panel_Left = Label(self.frame_Left, image=PILImage,width=480,height=240)
            self.panel_Left.image = PILImage
            self.panel_Left.grid(row=1, column=1, padx=10, pady=10)
            # set Histogram in Right panel bottom
            self.panel_LeftHisEqu = Figure(figsize=(4.8, 2.4), dpi=100)
            plot = self.panel_LeftHisEqu.add_subplot(111)
            plot.title.set_text('Image Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            self.canvasLeft = FigureCanvasTkAgg(self.panel_LeftHisEqu, self.frame_Left)
            self.canvasLeft.get_tk_widget().grid(row=2, column=1, padx=15, pady=5)
        else:
            # convert image to PIL then convert to ImageTk format
            PILImage = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
            # set image in Left panel
            self.panel_Left = Label(image=PILImage)
            self.panel_Left.image = PILImage
            self.panel_Left.pack(side="left", padx=10, pady=10)

    # set Right Image
    def setRightImage(self, image, event):
        # if not None clear Right panel
        if self.panel_Right != None or self.panel_RightHisEqu != None:
            self.canvasRight.get_tk_widget().destroy() if isinstance(self.panel_Right, Figure) else self.panel_Right.destroy()
            if isinstance(self.panel_RightHisEqu, Figure):
                self.canvasRight.get_tk_widget().destroy()
                self.frame_Right.destroy()
        # set image for download
        self.image_Right = image
        # convert color then resize image
        if event != "GaussianNoise" and event != "Wavelet" and event != "HistogramEqualization" and event != "convolution" and event != "OCR":
            image = self.resize(self.convertColor(image, cv2.COLOR_BGR2RGBA if event != "Histogram" else cv2.COLOR_BGR2GRAY), 480, 480)
        # if user want see histogram
        if event == "Histogram" or event == "GaussianNoise":
            # set Right panel is Figure
            self.panel_Right = Figure(figsize=(4.8, 4.8), dpi=100)
            # set Right panel plot
            plot = self.panel_Right.add_subplot(111)
            plot.title.set_text('Image Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            # set canvas
            self.canvasRight = FigureCanvasTkAgg(self.panel_Right, window)
            # set canvas position
            self.canvasRight.get_tk_widget().pack(side="right", padx=10, pady=10)
        elif event == "HistogramEqualization":
            # create frame
            self.frame_Right = Frame(window, background='#051636')
            self.frame_Right.pack(side=RIGHT)
            # convert image to PIL then convert to ImageTk format
            PILImage = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.resize(image, 480, 240)))
            # set image in Right panel top
            self.panel_Right = Label(self.frame_Right, image=PILImage,width=480,height=240)
            self.panel_Right.image = PILImage
            self.panel_Right.grid(row=1, column=1, padx=10, pady=10)
            # set Histogram in Right panel bottom
            self.panel_RightHisEqu = Figure(figsize=(4.8, 2.4), dpi=100)
            plot = self.panel_RightHisEqu.add_subplot(111)
            plot.title.set_text('Image Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            self.canvasRight = FigureCanvasTkAgg(self.panel_RightHisEqu, self.frame_Right)
            self.canvasRight.get_tk_widget().grid(row=2, column=1, padx=15, pady=5)
        elif event == "OCR":
            text = pytesseract.image_to_string(image, lang='eng')
            self.panel_Right = Text(window, height=350)
            self.panel_Right.pack(side="right", padx=10, pady=10)
            self.panel_Right.delete(1.0, END)
            self.panel_Right.insert(END, text)
            self.panel_Right.configure(state='disabled')
            # set button normal
            self.button_choise['state'] = NORMAL
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
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_ocr['state'] = NORMAL
            self.button_canny['state'] = DISABLED
            # image read by openCV
            self.image_original = cv2.imdecode(np.fromfile(self.imgPath, dtype=np.uint8), 1)
            # get image size
            self.size = self.image_original.shape
            # set two panel image
            self.setLeftImage(self.image_original, "Original")
            self.setRightImage(self.image_original, "Original")
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
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
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
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
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
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = NORMAL
            self.button_ocr['state'] = NORMAL
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = NORMAL
            self.button_ocr['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")

    # gaussian noise
    def gaussianNoise(self, SD):
        # set button disabled or normal
        self.button_choise['state'] = NORMAL
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
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
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
        # create object
        dialog = Dialog(window, '請輸入小波轉換層數')
        # wait window
        window.wait_window(dialog.top)
        # if answer is not none
        if dialog.ans != "" and dialog.ans.isdigit():
            # call harr function and set right image
            image = self.resize(self.convertColor(self.image_original, cv2.COLOR_BGR2GRAY), 480, 480)
            self.size = list(image.shape)
            self.image_Right = np.zeros((self.size[0], self.size[1]))
            for i in range(0, int(dialog.ans)):
                if i == 0:
                    self.haarDWT(image)
                else:
                    self.haarDWT(self.image_Right)
            # set left image
            self.setLeftImage(self.image_Left, "Gray")
            # set Right image
            self.setRightImage(self.image_Right, "Wavelet")
            # set button normal
            self.button_choise['state'] = NORMAL
        # if user click close button
        elif dialog.ans == "close":
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = NORMAL
            self.button_ocr['state'] = NORMAL
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = NORMAL
            self.button_ocr['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")
    
    # Harr Discrete Wavelet Transform
    def haarDWT(self, image):
        height = int(self.size[0] / 2)
        width = int(self.size[1] / 2)

        LL = np.zeros((height, width))
        LH = np.zeros((height, width))
        HH = np.zeros((height, width))
        HL = np.zeros((height, width))
        Lowpass = np.zeros((self.size[0], width))
        Highpass = np.zeros((self.size[0], width))

        for i in range (0, self.size[0]):
            for j in range(0, self.size[1], 2):
                Lowpass[i, int(j/2)] = int((image[i, j] / 2) + (image[i, j+1] / 2))
                Highpass[i, int(j/2)] = image[i, j] - Lowpass[i, int(j/2)]
        
        for i in range (0, Lowpass.shape[0], 2):
            for j in range(0, Lowpass.shape[1]):
                LL[int(i/2), j] = int((Lowpass[i, j]/2) + (Lowpass[i+1, j]/2))
                LH[int(i/2), j] = int((Lowpass[i, j]) - LL[int(i/2), j])
                HH[int(i/2), j] = int((Highpass[i, j]/2) + Highpass[i, j]/2)
                HL[int(i/2), j] = int(Highpass[i, j] - HL[int(i/2), j])
        
        LH[LH < 0] = 0
        LH = cv2.normalize(LH, None, 0, 255, cv2.NORM_MINMAX)
        HL[HL < 0] = 0
        HL = cv2.normalize(HL, None, 0, 255, cv2.NORM_MINMAX)
        HH[HH < 0] = 0
        HH = cv2.normalize(HH, None, 0, 255, cv2.NORM_MINMAX)

        self.image_Right[0:height, 0:width] = LL[:,:]
        self.image_Right[height:self.size[0], 0:width] = HL[:,:]
        self.image_Right[0:height, width:self.size[1]] = LH[:,:]
        self.image_Right[height:self.size[0], width:self.size[1]] = HH[:,:]

        self.size[0] = int(self.size[0] / 2)
        self.size[1] = int(self.size[1] / 2)
    
    # Histogram Equalization
    def histogramEqualization(self):
        # set button disabled
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        self.button_histogramEq['state'] = DISABLED
        image = self.resize(self.convertColor(self.image_original, cv2.COLOR_BGR2GRAY), 480, 480)
        hist, bins = np.histogram(image, 256)
        cdf = hist.cumsum()
        cdf = (cdf-cdf[0])*255/(cdf[-1]-1)
        cdf = cdf.astype(np.uint8)
        img2 = np.zeros((384, 495, 1), dtype =np.uint8)
        img2 = cdf[image]
        # set left image
        self.setLeftImage(self.image_original, "HistogramEqualization")
        # set right image
        self.setRightImage(img2, "HistogramEqualization")
    
    # Convolution
    def convolution(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
        # create object
        dialog = Dialog(window, '請輸入 mask 大小，以奇數為主\n(例如：輸入 5，即為 5 x 5 pixels)')
        # wait window
        window.wait_window(dialog.top)
        # if answer is not none
        if dialog.ans != "" and dialog.ans.isdigit() and int(dialog.ans) % 2 == 1:
            image = self.resize(self.convertColor(self.image_original, cv2.COLOR_BGR2GRAY), 480, 480)
            num = int(dialog.ans)
            kernel = num*num
            space = int((num-1)/2)
            temp = np.pad(image, int(num/2), mode='constant')
            height, width = temp.shape
            for i in range(0, height-num+1):
                for j in range(0, width-num+1):
                    image[i][j] = int((np.sum(temp[i : i+num , j : j+num]))/kernel)
            # set left image
            self.setLeftImage(self.image_Left, "Gray")
            # set Right image
            self.setRightImage(image, "convolution")
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_canny['state'] = NORMAL
        # if user click close button
        elif dialog.ans == "close":
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = DISABLED
            self.button_ocr['state'] = NORMAL
        elif int(dialog.ans) % 2 == 0:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = DISABLED
            self.button_ocr['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請盡可能輸入奇數")
        else:
            # set button normal
            self.button_choise['state'] = NORMAL
            self.button_histogram['state'] = NORMAL
            self.button_gaussianNoise['state'] = NORMAL
            self.button_waveletTrans['state'] = NORMAL
            self.button_histogramEq['state'] = NORMAL
            self.button_convolution['state'] = NORMAL
            self.button_canny['state'] = DISABLED
            self.button_ocr['state'] = NORMAL
            # show messagebox
            messagebox.showinfo("警告", "請勿輸入空值或輸入非數字")

    # Canny
    def canny(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        sobelr = np.array([[-1, 0, 1]], np.float32)
        sobelc = np.array([[1, 2, 1]], np.float32)
        Fx0 = np.zeros(shape = (self.image_Right.shape[0],self.image_Right.shape[1]-2))
        Fx = np.zeros(shape = (Fx0.shape[0]-2,Fx0.shape[1]))
        Fy0 = np.zeros(shape = (self.image_Right.shape[0],self.image_Right.shape[1]-2))
        Fy = np.zeros(shape = (Fy0.shape[0]-2,Fx0.shape[1]))

        for x in range(0, (self.image_Right.shape[0])):
            for y in range(0, (self.image_Right.shape[1]-2)):
                Fx0[x,y] = np.multiply(self.image_Right[x, y: y + 3], sobelr).sum()/8

        for x in range(0, (Fx0.shape[0]-2)):
            for y in range(0, (Fx0.shape[1])):
                Fx[x,y] = np.multiply(Fx0[x:x+3,y], sobelc).sum()/8

        for x in range(0, (self.image_Right.shape[0])):
            for y in range(0, (self.image_Right.shape[1]-2)):
                Fy0[x,y] = np.multiply(self.image_Right[x, y: y + 3], sobelc).sum()/8
            
        for x in range(0, (Fy0.shape[0]-2)):
            for y in range(0, (Fy0.shape[1])):
                Fy[x,y] = np.multiply(Fy0[x:x+3,y], sobelr).sum()/8
        
        sobel = np.sqrt(np.add(np.square(Fx), np.square(Fy)))
        sobel = sobel / sobel.max()*255
        theta = np.arctan2(Fx, Fy)

        height, width = sobel.shape
        Z = np.zeros((height, width), dtype=np.int32)
        angle = theta * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1, height-1):
            for j in range(1, width-1):
                try:
                    q = 255
                    r = 255

                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = sobel[i, j+1]
                        r = sobel[i, j-1]
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = sobel[i+1, j-1]
                        r = sobel[i-1, j+1]
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = sobel[i+1, j]
                        r = sobel[i-1, j]
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = sobel[i-1, j-1]
                        r = sobel[i+1, j+1]
                    
                    if (sobel[i,j] >= q) and (sobel[i,j] >= r):
                        Z[i,j] = sobel[i,j]
                    else:
                        Z[i,j] = 0
                except IndexError as e:
                    pass
        
        highThreshold = Z.max() * 0.09
        lowThreshold = highThreshold * 0.05
        M, N = Z.shape
        res = np.zeros((M,N), dtype=np.int32)
        weak = np.int32(25)
        strong = np.int32(255)

        strong_i, strong_j = np.where(Z >= highThreshold)
        zeros_i, zeros_j = np.where(Z < lowThreshold)
        weak_i, weak_j = np.where((Z <= highThreshold) & (Z >= lowThreshold))
        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak

        H, W = res.shape
        for i in range(1, H-1):
            for j in range(1, W-1):
                if (res[i,j] == 75):
                    try:
                        if ((res[i+1, j-1] == 100) or (res[i+1, j] == 100) or (res[i+1, j+1] == 100)
                            or (res[i, j-1] == 100) or (res[i, j+1] == 100) or (res[i-1, j-1] == 100)
                            or (res[i-1, j] == 100) or (res[i-1, j+1] == 100)): res[i, j] = 100
                        else:
                            res[i, j] = 0
                    except IndexError as e:
                        pass
        
        # set Right image
        self.setRightImage(res, "convolution")
        # set button normal
        self.button_choise['state'] = NORMAL

    # OCR
    def ocr(self):
        # set button disabled
        self.button_choise['state'] = DISABLED
        self.button_histogram['state'] = DISABLED
        self.button_gaussianNoise['state'] = DISABLED
        self.button_waveletTrans['state'] = DISABLED
        self.button_histogramEq['state'] = DISABLED
        self.button_convolution['state'] = DISABLED
        self.button_canny['state'] = DISABLED
        self.button_ocr['state'] = DISABLED
        image = self.convertColor(self.image_original, cv2.COLOR_BGR2GRAY) # 灰階
        image = cv2.convertScaleAbs(image, alpha = 1.8, beta = 0)
        blur = cv2.GaussianBlur(image, (3, 3), 0)
        ret, binary = cv2.threshold(blur, 190, 255, cv2.THRESH_TOZERO) # 二值化
        # set left image
        # self.setLeftImage(self.image_Left, "Gray")
        self.setLeftImage(self.resize(binary, 480, 480), "AlreadyGray")
        # set Right image
        self.setRightImage(binary, "OCR")

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
    imgProcessing.button_histogramEq = Button(frame_button, text="直方圖均化", highlightbackground='#051636', command=imgProcessing.histogramEqualization, state="disabled")
    imgProcessing.button_convolution = Button(frame_button, text="平滑化", highlightbackground='#051636', command=imgProcessing.convolution, state="disabled")
    imgProcessing.button_canny = Button(frame_button, text="邊緣偵測", highlightbackground='#051636', command=imgProcessing.canny, state="disabled")
    imgProcessing.button_ocr = Button(frame_button, text="圖轉文", highlightbackground='#051636', command=imgProcessing.ocr, state="disabled")
    # position
    imgProcessing.button_choise.grid(row=1, column=1, pady=20, padx=5)
    imgProcessing.button_histogram.grid(row=1, column=2, pady=20, padx=5)
    imgProcessing.button_gaussianNoise.grid(row=1, column=3, pady=20, padx=5)
    imgProcessing.button_waveletTrans.grid(row=1, column=4, pady=20, padx=5)
    imgProcessing.button_histogramEq.grid(row=1, column=5, pady=20, padx=5)
    imgProcessing.button_convolution.grid(row=1, column=6, pady=20, padx=5)
    imgProcessing.button_canny.grid(row=1, column=7, pady=20, padx=5)
    imgProcessing.button_ocr.grid(row=1, column=8, pady=20, padx=5)
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