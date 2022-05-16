import mysql.connector
from tkinter import *
from tkinter import ttk

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password ='AL38926516al',
    database='магазин'
)
cursor = mydb.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()

window = Tk()
window.title('Авторизация')
window.geometry('600x350')

frame = LabelFrame(window, text='Авторизация', font=30, labelanchor='n')
frame.pack(pady=55)

frame_into = Frame(frame)
frame_into.pack(pady=20)

arr = ['Логин', 'Пароль', 'Войти как']
for i in arr:
    Label(frame_into, text=i, font=3, width=8, anchor='e').grid(column=0, row=arr.index(i))
    if i == arr[-1]:
        arr = ['Администратор', 'Пароль', 'Клиент']
        for j in arr:
            Radiobutton(frame_into, text=j, font=3).grid(column=arr.index(j)+1, row=2)
    else:
        Entry(frame_into).grid(column=1, row=arr.index(i))

Button(frame, text='Войти', font=12, width=8).pack(side=BOTTOM, pady=15)

window.mainloop()