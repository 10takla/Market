import mysql.connector
from tkinter import *
from tkinter import ttk

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='AL38926516al',
    database='магазин'
)
cursor = mydb.cursor()

def destroy():
    children = window.winfo_children()
    for i in children:
        i.destroy()


window = Tk()

def admin(login):
    destroy()
    window.title('Администратор '+login)
    window.geometry('600x350')

    cursor.execute("SHOW TABLES FROM магазин;")
    db = cursor.fetchone()
    print(db)
    frame_panel = LabelFrame(window, text='Выберите таблицу', font=30, labelanchor='n')
    frame_panel.pack(pady=5, fill='x')

    for i in range(8):
        Button(frame_panel, text=i, font=8).pack(side=LEFT, padx=15, pady=10)

admin('adsda')

def into():
    def vhod(var, var2):
        if var[1].get() == '1':
            admin(var[0].get())
        elif var[1].get() == '2':
            pass
        else:
            pass

    window.title('Авторизация')
    window.geometry('600x350')

    frame = LabelFrame(window, text='Авторизация', font=30, labelanchor='n')
    frame.pack(pady=55)

    frame_into = Frame(frame)
    frame_into.pack(pady=20)

    arr = ['Логин', 'Пароль', 'Войти как']
    var = []
    var2 = []
    for i in arr:
        Label(frame_into, text=i, font=3, width=8, anchor='e').grid(column=0, row=arr.index(i))
        if i == arr[-1]:
            arr = ['Администратор', 'Пароль', 'Клиент']
            for j in arr:
                var2 += [IntVar]
                Radiobutton(frame_into, text=j, font=3, variable=var2, value=arr.index(j) + 1).grid(
                    column=arr.index(j) + 1, row=2)
        else:
            var += [StringVar()]
            Entry(frame_into, textvariable=var[arr.index(i)]).grid(column=1, row=arr.index(i))

    Label(frame, textvariable=var2).pack(side=LEFT)
    Button(frame, text='Войти', font=12, width=8, command=lambda: vhod(var, var2)).pack(side=BOTTOM, pady=15)


#into()

window.mainloop()
