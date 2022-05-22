import mysql.connector
from tkinter import *
from tkinter import ttk

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='AL38926516al',
    database='магазин'
)
mycursor = mydb.cursor()


def destroy(frame):
    children = frame.winfo_children()
    for i in children:
        i.destroy()


def get_columns_name(table):
    mycursor.execute(
        "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='магазин'  AND `TABLE_NAME`='" + table + "';")
    return [i for j in mycursor.fetchall() for i in j]

window = Tk()


def admin(login):
    destroy(window)
    window.title('Администратор ' + login)
    window.geometry('870x750')

    mycursor.execute("SHOW TABLES FROM магазин;")
    db = [i for j in mycursor.fetchall() for i in j]

    frame_panel = LabelFrame(window, text='Выберите таблицу', font=30, labelanchor='n')
    frame_panel.pack(pady=5, fill='x')
    for i in db:
        Button(frame_panel, text=i.title(), font=8, command=lambda i=i: (draw_table(i), draw_panel(i))).pack(side=LEFT, padx=15, pady=10)
    Button(frame_panel, text="Назад".title(), font=8, command=lambda: into()).pack(side=RIGHT, fill=Y)

    frame_table = Frame(window)
    frame_table.pack(anchor=W)
    def draw_table(table):
        destroy(frame_table)

        heads = get_columns_name(table)
        mycursor.execute("SELECT * FROM "+table+";")
        lst = mycursor.fetchall()
        table = ttk.Treeview(frame_table, show='headings')
        table['columns'] = heads

        for i in heads:
            table.heading(i, text=i.title().replace('_', ' '), anchor='center')
            table.column(i, anchor='center', width=100)
        for i in lst:
            table.insert('', END, values=i)

        scroll_pane = ttk.Scrollbar(frame_table, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=RIGHT, fill=Y)

        table.pack()
    draw_table(db[0])

    frame_edit = LabelFrame(window, text='Изменить', font=30)
    def draw_panel(table):
        destroy(frame_edit)
        frame_1 = Frame(frame_edit)
        frame_1.pack(anchor=W)

        bd = get_columns_name(table)
        for i in bd:
            Label(frame_1, text=i.title().replace('_', ' '), width=20, anchor=E).grid(row=bd.index(i), column=0)
            Entry(frame_1).grid(row=bd.index(i), column=1)

        arr = ["Добавить", "Изменить", "Удалить"]
        for i in arr:
            Button(frame_edit, text=i, font=2).pack(side=LEFT, anchor=S, padx=20)
        frame_edit.pack(pady=5, fill='x')
    draw_panel(db[0])

admin('adsda')


def into():
    destroy()

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


# into()

window.mainloop()
