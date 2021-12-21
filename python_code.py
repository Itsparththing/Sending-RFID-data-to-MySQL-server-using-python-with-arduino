from tkinter import *
import tkinter.messagebox
import mysql.connector
import serial
import time

con = mysql.connector.connect(host='localhost', password='123456789', user='root', database='safety')
cur = con.cursor()

# This will have to be changed to the serial port you are using
device = 'COM6'
print(("Trying..."),device)

arduino = serial.Serial(device, 9600)
CARD = arduino.readline()
print(CARD)
pieces = CARD.split(" ")

# This will check the reader has prior access of information or not
check = 'select cardno from info where(cardno='+str(CARD)
cur.execute(check)

if cur.fetchone():
    print("\033[1;34;47m*Card found in the Database*  \n")
else:
    print("\033[1;34;47m*Card not found in the Database*  \n")
    time.sleep(1)
    print('\033[1;34;47m~Card punched at new place~  \n')
    time.sleep(4)
    print('\033[2;30;47mCard Details:  \n')
    time.sleep(2)
    print(CARD)

    root = Tk()
    result = tkinter.messagebox.askquestion('Authentication!',
                                            'Some one wants your information. Do you want to give access?')
    if result == 'yes':
        theLabel = Label(root, text="Now he can access your information ")
        query = 'insert into info values ("{}",{},"{}",{})'.format("name, cardno, email, mobno")
        cur.execute(query)
        theLabel.pack()
    else:
        theLabel = Label(root, text="You denied the access")
        theLabel.pack()
    root.mainloop()

con.commit()
cur.execute(check)
