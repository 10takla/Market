import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb

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


def action(action, table, entries):
    if action == 'Добавить':
        text = get_columns_name(table)
        n = len(entries)
        for i in range(n):
            if entries[i] == '':
                del entries[i]
                del text[i]
        print(text, entries)

    elif action == "Изменить":
        pass
    elif action == "Удалить":
        print(action)


action('Добавить', 'клиент', ['', 'asd', '', ''])

window = Tk()


def worker(login, right):
    destroy(window)
    window.title(right + ' ' + login)
    window.minsize(200, 210)

    mycursor.execute("SHOW TABLES FROM магазин;")
    db = [i for j in mycursor.fetchall() for i in j]

    frame_panel = LabelFrame(window, text='Выберите таблицу', font=30, labelanchor='n')
    frame_panel.pack(pady=5, fill='x')
    for i in db:
        Button(frame_panel, text=i.title(), font=(1, 14), command=lambda i=i: (draw_table(i), draw_panel(i))).pack(
            side=LEFT, padx=15, pady=10)
    Button(frame_panel, text="Назад".title(), font=8, command=lambda: into()).pack(side=RIGHT, fill=Y)

    frame_table = Frame(window)
    frame_table.pack(anchor=W)

    def draw_table(table):
        destroy(frame_table)

        heads = get_columns_name(table)
        mycursor.execute("SELECT * FROM " + table + ";")
        lst = mycursor.fetchall()
        table = ttk.Treeview(frame_table, show='headings')
        table['columns'] = heads

        for i in heads:
            table.heading(i, text=i.title().replace('_', ' '), anchor='center')
            table.column(i, anchor='center', width=150)
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
        frame_1.pack(anchor=W, pady=20)

        bd = get_columns_name(table)
        var = []
        for i in bd:
            if right == 'Персонал' and table != 'продажа':
                continue
            Label(frame_1, text=i.title().replace('_', ' '), font=(1, 11), width=15, anchor=E).grid(row=bd.index(i),
                                                                                                    column=0)
            var += [StringVar()]
            Entry(frame_1, width=17, textvariable=var[bd.index(i)]).grid(row=bd.index(i), column=1)

        arr = ["Добавить", "Изменить", "Удалить"]
        for i in arr:
            if right == 'Персонал' and table != 'продажа':
                continue
            Button(frame_edit, text=i, font=(1, 12), command=lambda i=i: action(i, table, [i.get() for i in var])).pack(side=LEFT,
                                                                                                     anchor=S, padx=20,
                                                                                                     pady=10)
        frame_edit.pack(pady=5, fill='x')

    draw_panel(db[0])


def into():
    destroy(window)

    def vhod(var, var2, arr_2):
        if var[1].get() == '1' and var2 == arr_2[0]:
            worker(var[0].get(), var2)
        elif var[1].get() == '2' and var2 == arr_2[1]:
            worker(var[0].get(), var2)
        else:
            mb.showerror("Ошибка", "Неправильный логин или пароль!")

    window.title('Авторизация')
    window.minsize(600, 350)

    frame = LabelFrame(window, text='Авторизация', font=30, labelanchor='n')
    frame.pack(pady=55)

    frame_into = Frame(frame)
    frame_into.pack(pady=20)

    arr = ['Логин', 'Пароль', 'Войти как']
    var = []
    for i in arr:
        Label(frame_into, text=i, font=3, width=8, anchor='e').grid(column=0, row=arr.index(i))
        if i != arr[-1]:
            var += [StringVar()]
            Entry(frame_into, textvariable=var[arr.index(i)]).grid(column=1, row=arr.index(i))
        else:
            arr_2 = ['Администратор', 'Персонал', 'Клиент']
            var2 = IntVar()
            for j in arr_2:
                Radiobutton(frame_into, text=j, font=3, variable=var2, value=arr_2.index(j)).grid(
                    column=arr_2.index(j) + 1, row=2)

    Button(frame, text='Войти', font=12, width=8, command=lambda: vhod(var, arr_2[var2.get()], arr_2)).pack(side=BOTTOM,
                                                                                                            pady=15)


#into()

window.mainloop()
