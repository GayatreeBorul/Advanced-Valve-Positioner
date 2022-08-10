import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter.messagebox import showerror
from PIL import ImageTk, Image

# define a video capture object
vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('im.png', frame)
        break

# After the loop release the cap object
vid.release()
#cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
im = cv2.imread("im.png")                        # Read image
imS = cv2.resize(im, (529,423))                    # Resize image
#cv2.imshow("output", imS)                            # Show image
cv2.imwrite('im1.png',imS)
cv2.waitKey(0)
# Read image
image = cv2.imread('im1.png', cv2.IMREAD_GRAYSCALE)
height = image.shape[1]
width = image.shape[1]
cv2.imwrite("new.png", image)
cv2.imshow("Image", image)
originalImage = cv2.imread('new.png')
slicedImage = originalImage[196:360,270:290]
cv2.imwrite("new1.png", slicedImage)
cv2.imshow("new1.png",slicedImage)
Image1 = cv2.imread('new1.png')

##converted grey img into black and white
(thresh, blackAndWhiteImage) = cv2.threshold(Image1, 128, 255, cv2.THRESH_BINARY)
cv2.imwrite("black&white.jpg", blackAndWhiteImage)
cv2.imshow("black&white.jpg", blackAndWhiteImage)
mask = cv2.imread('black&white.jpg')
gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    # draw the center of the shape on the image
    cv2.circle(mask, (cX, cY), 5, (0, 0, 255), 1)
    # show the image
    P = cY * (164/131.2 )
    print(cY)
    measured_value = 100 - (P / 2)
    print('Valve is open( in % ):', measured_value)

    #################################################################table#############################################
    ## to enter total time needed from 0 to 100 %
    Total_time = 30  ####optional

window = Tk()
window.title('READING OF VERTICAL VALVE POSITIONE')
window.geometry('600x800')

frame2 = Frame(window,height = 400, width = 500)
frame1 = Frame(window)
frame3 = Frame(window)
frame4 = Frame(window)
frame5 = Frame(window)

frame1.grid(row = 1, column = 0)
frame2.grid(row = 2, column = 0)
frame3.grid(row = 3, column = 0)
frame4.grid(row = 4, column = 0)
frame5.grid(row = 5, column = 0)

my_img = ImageTk.PhotoImage(Image.open('im1.png'))
my_label = Label(frame2, image=my_img)
my_label.grid(row=5, column=3)


class Table:

    def __init__(self, frame2):
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(frame1, width=20, fg='blue', font=('Times New Roman', 12, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


# take the data
lst = [('Specification', 'Unit', 'Values'), ('Measured Value', '%', measured_value),
       ('Total Opening Time', 'sec', Total_time), ('Total Closing Time', 'sec', Total_time)]
# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])
# create root window
t = Table(frame1)


setpoint_label = Label(frame3, text="ENTER THE SET POINT(%)", borderwidth=2, relief="raised",font=('Times New Roman', 11, 'bold'))
setpoint_label.grid(row=4, column=0, ipadx=1)
setpoint = StringVar()
setpoint_entry = Entry(frame3, textvariable=setpoint, borderwidth=2, relief="raised",font=('Times New Roman', 11, 'bold'))
setpoint_entry.grid(row=4, column=1, ipadx=1)

setpoint_entry.focus()


def instruction(Set_point):
    measured_Time = (float(Total_time * (float(measured_value)))) / 100
    set_time = (Set_point * Total_time) / 100
    return float(set_time - measured_Time)

    #if (Set_point > measured_value):
         #R = set_time - measured_Time
         #print('Open the valve for seconds \n',R )
    #elif (Set_point == measured_value):
        #print('given valve meets the required set point condition.\n')
    #else:
        #U = measured_Time - set_time
        #print('close the valve for ', U, 'seconds \n')


def button():
        try:
            Set_point = float(setpoint.get())
            final_result = instruction(Set_point)
            if final_result>0:
             result.insert(INSERT, "\nOpen the air valve\n",INSERT, final_result) #positive value = open air valve
            else:
             result.insert(INSERT, "\nOpen the vent valve\n", INSERT,final_result)#Negative value=open vent valve




        except ValueError as error:
            messagebox.showerror(title='Error', message='error')




button = Button(frame3, text="SUBMIT", command=button,bg='green', font=('Times New Roman', 11, 'bold'))
button.grid(row=4, column=2, ipadx=1, sticky=W)
# result label-
result= Text(frame4,height=5,width=45, bg='white',fg='black',font=("Times New Roman",13,"bold"),bd=5)
result.grid(row=6,column=3,padx=3)
# for exit button
button_quit = Button(frame5, text='Exit', command=window.quit,bg='red',font=('Times New Roman', 11, 'bold'))
button_quit.grid(row=7, column=3, ipadx=2, sticky=S)

cv2.waitKey(0)
window.mainloop()
