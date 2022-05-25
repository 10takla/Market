import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='KKKasl',
    database='магазин'
)
mycursor = mydb.cursor()


def destroy(frame):
    children = frame.winfo_children()
    for i in children:
        i.destroy()


def get_columns_name(table, column_delete=''):
    if column_delete != '':
        column_delete = " AND `COLUMN_NAME` NOT IN(" + column_delete + ")"
    mycursor.execute(
        "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='магазин' AND `TABLE_NAME`='" + table + "'" + column_delete + ";")
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

        if entries[0] == '':
            mb.showerror("Ошибка", "Введите id строки!")
        else: mycursor.execute(
            "UPDATE " + table + " SET " + text_3 + " WHERE (" + text[0] + " = '" + entries[0] + "');")

    elif action == "Удалить":
        if entries[0] == '':
            mb.showerror("Ошибка", "Введите id строки!")
        else: mycursor.execute("DELETE FROM " + table + " WHERE " + text[0] + " = " + entries[0] + ";")


def draw_table(frame_table, table, text, column_delete=''):
    destroy(frame_table)
    heads = get_columns_name(table, column_delete)
    mycursor.execute(text)
    lst = mycursor.fetchall()
    table = ttk.Treeview(frame_table, show='headings', columns=heads, height=20)

    for i in heads:
        table.heading(i, text=i.title().replace('_', ' '))
        table.column(i, anchor=W, width=150)
    for i in lst:
        table.insert('', END, values=i)

    scroll_pane = ttk.Scrollbar(frame_table, command=table.yview)
    table.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=RIGHT, fill=Y)

    table.pack()


window = Tk()
color = ['#f75252', '#ffffff', '#adcfff']


def worker(login, right):
    destroy(window)
    window.title(right + ' ' + login)
    window.minsize(200, 210)

    mycursor.execute("SHOW TABLES FROM магазин;")
    db = [i for j in mycursor.fetchall() for i in j]

    frame_panel = LabelFrame(window, text='Выберите таблицу', font=30, labelanchor='n')
    frame_panel.pack(pady=5, fill='x')
    for i in db:
        Button(frame_panel, relief=GROOVE, text=i.title(), font=(1, 14),
               command=lambda i=i: (draw_table(frame_table, i, "SELECT * FROM " + i + ";"), draw_panel(i))).pack(
            side=LEFT, padx=15, pady=10)
    Button(frame_panel, relief=RAISED, text="Выйти".title(), font=8, command=lambda: into()).pack(side=RIGHT, fill=Y)

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
                   command=lambda i=i: (action(i, table, [i.get() for i in var]), draw_table(frame_table, table, "SELECT * FROM " + table + ";"))).pack(
                side=LEFT,
                anchor=S, padx=10,
                pady=10)
        frame_edit.pack(pady=5, fill='x')

    draw_panel(db[0])


def client(login):
    def where(search, var_1, var_2, var_3, arr):
        text = ['назвакние_товара LIKE "_%' + search.get() + '_%"']

        if var_1[0].get() == 1 and var_1[1].get() == 0:
            text += ["в_наличии != '0'"]
        elif var_1[0].get() == 0 and var_1[1].get() == 1:
            text += ["в_наличии = '0'"]

        if var_2[0].get() < var_2[1].get():
            text += ["цена BETWEEN " + str(var_2[0].get()) + " and " + str(var_2[1].get())]

        def add(text):
            tmp1 = []
            for i in var_3:
                tmp2 = []
                for j in i:
                    if j.get() != '':
                        tmp2 += [f"'{j.get()}'"]
                tmp1 += [tmp2]
            for i in arr:
                if i == arr[0] and tmp1[0] != []:
                    text += ["категория IN(" + ", ".join(tmp1[0]) + ")"]
                if i == arr[1] and tmp1[1] != []:
                    text += [
                        "id_производителя IN (SELECT id_производителя FROM производитель WHERE фирма IN(" + ", ".join(
                            tmp1[1]) + "))"]
            return text

        add(text)

        if len(text) == 0:
            return ''
        else:
            return (' WHERE ' + ' and '.join(text))

    def order(var_4):
        text = []
        if var_4.get() == 'Сначала дорогие':
            text += ["цена DESC"]
        elif var_4.get() == 'Сначала дешевые':
            text += ["цена ASC"]
        if len(text) == 0:
            return ''
        else:
            return (' ORDER BY ' + ' and '.join(text))

    def group(var_4):
        text = []
        if var_4.get() == 'По id':
            text += ["id_товара"]
        elif var_4.get() == 'По производителю':
            text += ["id_производителя"]
        elif var_4.get() == 'По категории':
            text += ["категория"]

        if len(text) == 0:
            return ''
        else:
            return (' GROUP BY ' + ' and '.join(text))

    destroy(window)
    window.title('Клиент ' + login)
    window.minsize(200, 210)
    padx, pady = 10, 6

    frame_search = LabelFrame(window, text='Поиск', font=(1, 15))
    frame_search.pack(side=TOP, anchor=W, padx=20, pady=15)

    search = StringVar()
    Entry(frame_search, textvariable=search).pack(side=LEFT)

    column_delete = "'id_поставки'"
    t = get_columns_name('товар')
    t.remove('id_поставки')
    t = ", ".join(t)
    Button(frame_search, text='Поиск', font=(1, 11), command=lambda: draw_table(frame_table, 'товар',
                                                                                "SELECT " + t + " FROM товар " + where(
                                                                                    search, var, var_2, var_3,
                                                                                    arr) + group(var_4[1]) + order(
                                                                                    var_4[0]) + ";",
                                                                                column_delete)).pack(
        padx=10, side=LEFT)
    Button(frame_search, relief=RAISED, text='Выйти', font=(1, 11), command=lambda: into()).pack()

    frame_filter = LabelFrame(window, text='Фильтры', font=(1, 15), labelanchor=N)
    frame_filter.pack(anchor=W, padx=20, side=LEFT)

    arr = ["В наличии", "Отсутсвует в наличии"]
    var = []
    for i in arr:
        var += [IntVar()]
        Checkbutton(frame_filter, text=i, variable=var[arr.index(i)]).pack(anchor=W, padx=padx)

    frame_price = LabelFrame(frame_filter, text='Цена', font=(1, 13))
    frame_price.pack(padx=padx, pady=pady)
    array = ['От', 'До']
    var_2 = []
    for i in array:
        Label(frame_price, text=i).pack(side=LEFT)
        var_2 += [IntVar()]
        Spinbox(frame_price, from_=0, to=100000, increment=1000, width=7, textvariable=var_2[array.index(i)]).pack(
            side=LEFT)

    arr = ['Категория', 'Производитель']
    arr_2 = ['категория', 'фирма']
    arr_3 = ['товар', 'производитель']
    var_3 = []
    for i in arr:
        frame_1 = LabelFrame(frame_filter, text=i, font=(1, 13))
        frame_1.pack(anchor=W, padx=padx, pady=pady)
        mycursor.execute("SELECT " + arr_2[arr.index(i)] + " FROM " + arr_3[arr.index(i)] + ";")
        l = list(set(i for j in mycursor.fetchall() for i in j))
        tmp = []
        for i in l:
            tmp += [StringVar()]
            Checkbutton(frame_1, text=i, variable=tmp[l.index(i)], onvalue=i, offvalue='').pack(anchor=W)
        var_3 += [tmp]

    arr_4 = ['Сортировка', 'Группировка']
    arr_5 = [('Отсутсвует', 'Сначала дорогие', 'Сначала дешевые'),
             ('Отсутсвует', 'По id', 'По производителю', 'По категории')]
    var_4 = []
    for i in arr_4:
        frame_2 = LabelFrame(frame_filter, text=i, font=(1, 13))
        frame_2.pack(anchor=W, padx=padx, pady=3)
        var_4 += [StringVar()]
        ttk.Combobox(frame_2, textvariable=var_4[arr_4.index(i)], values=arr_5[arr_4.index(i)]).pack()

    frame_table = Frame(window)
    frame_table.pack(anchor=W)
    draw_table(frame_table, 'товар', "SELECT " + t + " FROM " + 'товар' + ";", column_delete)

def into():
    destroy(window)

    def vhod(var, var2):
        if var[0].get() == '' and var[1].get() != '':
            mb.showwarning("Ошибка", "Введите логин")
        elif var[1].get() == '1' and var2 == 'Администратор':
            worker(var[0].get(), var2)
        elif var[1].get() == '2' and var2 == 'Персонал':
            worker(var[0].get(), var2)
        elif var2 == 'Клиент':
            client(var[0].get())
        else:
            mb.showerror("Ошибка", "Неправильный логин или пароль!")

    window.title('Вход')
    window.minsize(600, 350)

    frame = LabelFrame(window, text='Авторизация', font=(1, 17), labelanchor='n')
    frame.pack(pady=55)

    frame_into = Frame(frame)
    frame_into.pack(pady=20)

    arr = ['Логин', 'Пароль', 'Войти как']
    var = []
    for i in arr:
        Label(frame_into, text=i, font=(1, 12), width=8, anchor='e').grid(column=0, row=arr.index(i))
        if i != arr[-1]:
            var += [StringVar()]
            Entry(frame_into, textvariable=var[arr.index(i)]).grid(column=1, row=arr.index(i))
        else:
            arr_2 = ['Администратор', 'Персонал', 'Клиент']
            var2 = IntVar()
            for j in arr_2:
                Radiobutton(frame_into, text=j, font=(1, 12), variable=var2, value=arr_2.index(j)).grid(
                    column=arr_2.index(j) + 1, row=2)

    Button(frame, relief=GROOVE, text='Войти', font=(1, 12), width=8, command=lambda: vhod(var, arr_2[var2.get()])).pack(side=BOTTOM,
                                                                                                     pady=15)


into()

window.mainloop()
