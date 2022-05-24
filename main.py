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
    text = get_columns_name(table)
    text_1 = []
    text_2 = []
    for i in range(len(entries)):
        if entries[i] != '':
            text_1.append(text[i])
            text_2.append(entries[i])

    if action == 'Добавить':
        text_1 = ", ".join([i for i in text_1])
        text_2 = ", ".join([f"'{i}'" for i in text_2])
        mycursor.execute("INSERT INTO " + table + " (" + text_1 + ") VALUES (" + text_2 + ");")

    elif action == "Изменить":
        text_1.pop(0)
        text_2.pop(0)
        text_2 = [f"'{i}'" for i in text_2]
        text_3 = []
        for i in range(len(text_1)):
            text_3 += [text_1[i] + " = " + text_2[i]]
        text_3 = ", ".join(text_3)
        mycursor.execute(
            "UPDATE " + table + " SET " + text_3 + " WHERE (" + text[0] + " = '" + entries[0] + "');")
        if entries[0] == '':
            mb.showerror("Ошибка", "Введите id строки!")

    elif action == "Удалить":
        mycursor.execute("DELETE FROM " + table + " WHERE " + text[0] + " = " + entries[0] + ";")
        if entries[0] == '':
            mb.showerror("Ошибка", "Введите id строки!")


def draw_table(frame_table, table, text):
    destroy(frame_table)

    heads = get_columns_name(table)
    mycursor.execute(text)
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
        Button(frame_panel, text=i.title(), font=(1, 14),
               command=lambda i=i: (draw_table(frame_table, i, "SELECT * FROM " + i + ";"), draw_panel(i))).pack(
            side=LEFT, padx=15, pady=10)
    Button(frame_panel, text="Выйти".title(), font=8, command=lambda: into()).pack(side=RIGHT, fill=Y)

    frame_table = Frame(window)
    frame_table.pack(anchor=W)
    draw_table(frame_table, db[0], "SELECT * FROM " + db[0] + ";")

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
            Button(frame_edit, text=i, font=(1, 12),
                   command=lambda i=i: (action(i, table, [i.get() for i in var]), draw_table(table))).pack(
                side=LEFT,
                anchor=S, padx=20,
                pady=10)
        frame_edit.pack(pady=5, fill='x')

    draw_panel(db[0])


def client(login):
    def power(var_1, var_2, var_3):
        print(var_3)
        for i in range(len(var_2)):
            print(var_2[i])
        if var_1[0].get() == 1 and var_1[1].get() == 0:
            return (" WHERE в_наличии = '0'")
        elif var_1[0].get() == 0 and var_1[1].get() == 1:
            return (" WHERE в_наличии != '0'")
        else: return ''
    destroy(window)
    window.title('Клиент ' + login)
    window.minsize(200, 210)

    frame_search = LabelFrame(window, text='Поиск', font=(1, 15))
    frame_search.pack(side=TOP, anchor=W, padx=20, pady=15)
    Entry(frame_search).pack(side=LEFT)
    Button(frame_search, text='Поиск', font=(1, 11), command=lambda: draw_table(frame_table, 'товар', "SELECT * FROM товар "+power(var, var_2, var_3)+";") ).pack(padx=10, side=LEFT)
    Button(frame_search, text='Выйти', font=(1, 11), command=lambda: into()).pack()


    frame_filter = LabelFrame(window, text='Фильтры', font=(1, 15), labelanchor=N)
    frame_filter.pack(anchor=W, padx=20, side=LEFT)

    arr = ["В наличии", "Отсутсвует в наличии"]
    var = []
    for i in arr:
        var += [IntVar()]
        Checkbutton(frame_filter, text=i, variable=var[arr.index(i)]).pack(anchor=W)

    frame_price = LabelFrame(frame_filter, text='Цена', font=(1, 13))
    frame_price.pack()
    array = ['От', 'До']
    var_2 = []
    for i in array:
        Label(frame_price, text=i).pack(side=LEFT)
        t=Spinbox(frame_price, from_=0, to=100000, increment=1000, width=7)
        t.pack(side=LEFT)
        var_2 += [t.get()]

    arr = ['Категория', 'Производитель']
    arr_2 = ['категория', 'фирма']
    arr_3 = ['товар', 'производитель']
    var_3 = []
    for i in arr:
        frame_1 = LabelFrame(frame_filter, text=i, font=(1, 13))
        frame_1.pack(anchor=W)
        mycursor.execute("SELECT " + arr_2[arr.index(i)] + " FROM " + arr_3[arr.index(i)] + ";")
        l = set(mycursor.fetchall())
        var_3 += [('')]
        for i in l:
            var_3 += [(1)]
            Checkbutton(frame_1, text=i, variable=var).pack(anchor=W)

    arr_4 = ['Сортировка', 'Группировка']
    arr_5 = [('Отсутсвует', 'Сначала дорогие', 'Сначала дешевые'),
             ('Отсутсвует', 'По id', 'По производителю', 'По категории')]
    for i in arr_4:
        frame_2 = LabelFrame(frame_filter, text=i, font=(1, 13))
        frame_2.pack(anchor=W)
        ttk.Combobox(frame_2, values=arr_5[arr_4.index(i)]).pack()

    frame_table = Frame(window)
    frame_table.pack(anchor=W)
    draw_table(frame_table, 'товар', "SELECT * FROM " + 'товар'+";")


client('')


def into():
    destroy(window)

    def vhod(var, var2):
        if var[1].get() == '1' and var2 == 'Администратор':
            worker(var[0].get(), var2)
        elif var[1].get() == '2' and var2 == 'Персонал':
            worker(var[0].get(), var2)
        elif var2 == 'Клиент':
            client(var[0].get())
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

    Button(frame, text='Войти', font=12, width=8, command=lambda: vhod(var, arr_2[var2.get()])).pack(side=BOTTOM,
                                                                                                     pady=15)


# into()

window.mainloop()
