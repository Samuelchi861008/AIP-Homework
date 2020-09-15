from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# 建立主視窗
window = Tk()
# 設定視窗標題
window.title('AIP 60947017S')
# 設定視窗大小
window.geometry('800x600')
# 設定背景顏色
window.configure(background='#3E4149')

# 圖片上傳
def upload():
    filename = filedialog.askopenfilename(title='open')
    img = Image.open(filename)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img
    panel.pack()

# 主程式
def main():
    # 建立按鈕 (按鈕所在視窗, 顯示文字, 按下按鈕所執行的函數)
    button = Button(window, text = "上傳圖片", highlightbackground='#3E4149', command = upload)
    # 以預設方式排版按鈕
    button.pack(side=TOP)

    # 運行主程式
    window.mainloop()

if __name__ == '__main__':
    main()