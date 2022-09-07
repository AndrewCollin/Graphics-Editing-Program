from PIL import Image, ImageEnhance, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

path = "C:/Users/Syste/Documents/Comics"

def makeDir(name):
    try:
        os.mkdir(path + "/" + name)
    except OSError:
        print("File already exists")
    else:
        print("file created successfully")
    try:
        os.mkdir(path + "/" + name + "/Webtoons")
        os.mkdir(path + "/" + name + "/Instagram")
    except OSError:
        print("A cropped comic already exists")
    else:
        print("Preparing Directory")


def fourPanelCrop(image, name):
    # image.crop((left,top,right,lower))
    # 1432 x 1432 is the size of the border
    # 3300 x 3300 is the size of a 4 panel comic

    side = 178
    top = 183
    boxDim = 1431
    border = 60

    panel1 = image.crop(
        (side - border, top - border, side + boxDim + border, top + boxDim + border))  # Difference of 1575
    # panel1.show()
    panel2 = image.crop(
        (3300 - side - boxDim - border, top - border, 3300 - side + border, top + boxDim + border))
    # anel2.show()
    panel3 = image.crop(
        (side - border, 3300 - top - boxDim - border, side + boxDim + border, 3300 - top + border))
    # panel3.show()
    panel4 = image.crop(
        (3300 - side - 1431 - border, 3300 - top - boxDim - border, 3300 - side + border, 3300 - top + border))
    # panel4.show()

    instaPath = path + "/" + name + "/Instagram"
    panel1.save(instaPath + "/panel1" + ".png")
    panel2.save(instaPath + "/panel2" + ".png")
    panel3.save(instaPath + "/panel3" + ".png")
    panel4.save(instaPath + "/panel4" + ".png")

    webPath = path + "/" + name + "/Webtoons"
    panel1.resize((790, 790)).convert('RGB').save(webPath + "/panel1" + ".jpg")
    panel2.resize((790, 790)).convert('RGB').save(webPath + "/panel2" + ".jpg")
    panel3.resize((790, 790)).convert('RGB').save(webPath + "/panel3" + ".jpg")
    panel4.resize((790, 790)).convert('RGB').save(webPath + "/panel4" + ".jpg")


def fivePanelCrop(image, name, height):
    fourPanelCrop(image, name)
    top = 190
    boxDim = 1431
    side = 934
    border = 60
    panel5 = image.crop(
        (side - border, height - 183 - boxDim - border, 3300 - side + border, height - top + border))
    instaPath = path + "/" + name + "/Instagram"
    panel5.save(instaPath + "/panel5" + ".png")
    webPath = path + "/" + name + "/Webtoons"
    panel5.resize((790, 790)).convert('RGB').save(webPath + "/panel5" + ".jpg")

def imageContrast(image,name):
    contrastFactor = 1.3
    img = image
    imgCon = ImageEnhance.Contrast(img)
    img = imgCon.enhance(contrastFactor)
    try:
        os.mkdir(path + "/" + name + "/ImageContrast")
    except OSError:
        print("A cropped comic already exists")
        messagebox.showerror("Error", "A cropped comic already exists")
    else:
        print("Preparing Directory")

    conPath = path + "/" + name + "/ImageContrast"
    img.save(conPath + "/" + name + ".png")

def implimentImage(name, dir):
    image = dir
    width, height = image.size

    print(height)

    makeDir(name)
    # If 4 panel comic
    if width == height:
        image.save(path + "/" + name + "/" + name + ".png")
        dImage = ImageDraw.Draw(image)
        dImage.line((0, 3200, 3300, 3200), fill="white", width=140)
        fourPanelCrop(image, name)
    else:
        image.save(path + "/" + name + "/" + name + ".png")
        dImage = ImageDraw.Draw(image)
        dImage.line((0, height - 100, height, height - 100), fill="white", width=140)
        fivePanelCrop(image, name, height)

    imageContrast(image,name)

def browseFunction():
    browseText.delete(0,tk.END)
    fileName = tk.filedialog.askopenfilename(initialdir = "/",
                                             filetypes=[("Image File",'.jpg .png .jpeg')])
    browseText.insert(0, fileName)
    preImage = Image.open(fileName).resize((400,400))
    newImage = ImageTk.PhotoImage(preImage)
    imageLabel.configure(image=newImage)
    imageLabel.image = newImage

def crop():
    fileName = browseText.get()
    titleCrop = titleInput.get()
    if titleCrop == "":
        messagebox.showerror("Value Error", "Please enter a title")
        return
    if not os.path.isfile(fileName):
        messagebox.showerror("Value Error", "Please select a photo you want to crop")
        return
    implimentImage(titleCrop,Image.open(fileName))
    pb['text'] = "Image processing done"
def exitButton():
    window.destroy()


window = tk.Tk()
fileName = None
window.title("Cut-It by Andrew Collin")
graphicFrame = tk.Frame()
noImage = ImageTk.PhotoImage(Image.open("noImage.png").resize((400,400)))
imageLabel = tk.Label(graphicFrame, image = noImage)
imageLabel.pack()
graphicFrame.pack(padx = 20, pady = (20,0))
lineDivider = ttk.Separator(window, orient='horizontal')
lineDivider.pack(fill = 'x', padx=20, pady=10)
frame = tk.Frame()
browseButton = tk.Button(frame, text = "Browse", command = browseFunction)
browseButton.grid(row = 0, column = 0)
browseText = tk.Entry(frame, width = 40)
browseText.grid(row = 0, column = 1)
browseText.insert(0, "C:")
title = tk.Label(frame, text = "Title:")
title.grid(row=1,column=0)
titleInput = tk.Entry(frame, width = 40)
titleInput.grid(row = 1, column = 1)
ccFrame = tk.Frame(window)
checkBoxFrame = tk.Frame(ccFrame)
var1, var2, var3, var4, var5, var6 = tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()
bottomFrame = tk.Frame(ccFrame)
cropButton = tk.Button(bottomFrame, text = "Crop!", command = crop, width = 10, height = 5)
exitButton = tk.Button(bottomFrame, text="Exit", command = exitButton, width = 10, height = 5)
cropButton.grid(row = 0, column = 0)
exitButton.grid(row = 0, column = 1)
bottombFrame = tk.Frame(window)
pb = tk.Label(bottombFrame,text="", fg = "SpringGreen4")
pb.pack()

window.resizable(False,False)
frame.pack(padx = 20)
checkBoxFrame.grid(row = 0, column = 0, padx = 20,pady=10)
bottomFrame.grid(row=0, column = 1, padx = 20)
ccFrame.pack()
bottombFrame.pack(padx = 20, pady = (0,20))
window.bind('<Return>', lambda e: crop())
window.mainloop()
