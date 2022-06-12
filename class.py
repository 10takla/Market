import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb

connect_bd = [i.replace('\n', '') for i in open("host_connect.txt", encoding='utf-8')]

mydb = mysql.connector.connect(
    host=connect_bd[0].split(': ')[1],
    user=connect_bd[1].split(': ')[1],
    password=connect_bd[2].split(': ')[1],
    database=connect_bd[3].split(': ')[1]
)
mycursor = mydb.cursor()


def destroy(frame):
    children = frame.winfo_children()
    for i in children:
        i.destroy()


def get_columns_name(table, column_delete=''):
    if column_delete != '':
        column_delete = " AND COLUMN_NAME NOT IN(" + column_delete + ")"
        mycursor.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME`='" + table + "'" + column_delete + ";")
    else:
        mycursor.execute("SHOW COLUMNS FROM " + table + ";")
    return [i for j in mycursor.fetchall() for i in j if j.index(i) == 0]


def draw_table(frame_table, columns, text):
    destroy(frame_table)

    mycursor.execute(text)
    data = mycursor.fetchall()

    table = ttk.Treeview(frame_table, show='headings', columns=columns, height=20)
    for i in columns:
        table.heading(i, text=i.title().replace('_', ' '))
        table.column(i, anchor=W, width=150)
    for i in data:
        table.insert('', END, values=i)

    scroll_pane = ttk.Scrollbar(frame_table, command=table.yview)
    table.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=RIGHT, fill=Y)

    table.pack()


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
        else:
            mycursor.execute(
                "UPDATE " + table + " SET " + text_3 + " WHERE (" + text[0] + " = '" + entries[0] + "');")

    elif action == "Удалить":
        if entries[0] == '':
            mb.showerror("Ошибка", "Введите id строки!")
        else:
            mycursor.execute("DELETE FROM " + table + " WHERE " + text[0] + " = " + entries[0] + ";")


def authorization(type, passwords, rights, rights_attributes):
    destroy(window)
    window.title('Вход')
    window.minsize(600, 350)

    frame = LabelFrame(window, text='Авторизация', font=(1, 17), labelanchor='n')
    frame.pack(pady=55)

    frame_into = Frame(frame)
    frame_into.pack(pady=20)

    arr = ['Логин', 'Пароль', 'Войти как']
    log_pass = []
    for i in arr:
        Label(frame_into, text=i, font=(1, 12), width=8, anchor='e').grid(column=0, row=arr.index(i))
        if i != arr[-1]:
            log_pass += [StringVar()]
            Entry(frame_into, textvariable=log_pass[arr.index(i)]).grid(column=1, row=arr.index(i))
        else:
            index_type = IntVar()
            for j in type:
                Radiobutton(frame_into, text=j, font=(1, 12), variable=index_type, value=type.index(j)).grid(
                    column=type.index(j) + 1, row=2)

    Button(frame, relief=GROOVE, text='Войти', font=(1, 12), width=8,
           command=lambda: vhod([i.get() for i in log_pass], index_type.get())).pack(side=BOTTOM, pady=15)

    def vhod(log_pass, index_type):
        if log_pass[0] == '':
            mb.showwarning("Ошибка", "Введите логин")

        elif (rights[index_type] == 1 or rights[index_type] == 2) and log_pass[1] != passwords[
            index_type]:
            mb.showerror("Ошибка", "Неправильный логин или пароль!")
        else:
            work(type, index_type, log_pass[0], rights, rights_attributes)


def work(type, index_type, login, rights, rights_attributes):
    destroy(window)
    window.title(type[index_type] + ' ' + login)
    window.minsize(200, 210)
    if rights[index_type] in [1, 2]:
        mycursor.execute("SHOW TABLES FROM " + connect_bd[3].split(': ')[1] + ";")
        db = [i for j in mycursor.fetchall() for i in j]

        frame_panel = LabelFrame(window, text='Выберите таблицу', font=30, labelanchor='n')
        frame_panel.pack(pady=5, fill='x')
        for i in db:
            Button(frame_panel, relief=GROOVE, text=i.title(), font=(1, 14),
                   command=lambda i=i: (
                   draw_table(frame_table, get_columns_name(i), "SELECT * FROM " + i + ";"), draw_panel(i))).pack(
                side=LEFT, padx=15, pady=10)

        frame_table = Frame(window)
        frame_table.pack(anchor=W)
        draw_table(frame_table, get_columns_name(db[0]), "SELECT * FROM " + db[0] + ";")

        frame_edit = LabelFrame(window, text='Изменить', font=30)

        def draw_panel(table):
            destroy(frame_edit)
            frame_1 = Frame(frame_edit)
            frame_1.pack(anchor=W, pady=20)

            bd = get_columns_name(table)
            var = []
            for i in bd:
                if rights[index_type] == 2 and table not in rights_attributes[index_type]:
                    continue
                Label(frame_1, text=i.title().replace('_', ' '), font=(1, 11), width=15, anchor=E).grid(row=bd.index(i),
                                                                                                        column=0)
                var += [StringVar()]
                Entry(frame_1, width=17, textvariable=var[bd.index(i)]).grid(row=bd.index(i), column=1)

            arr = ["Добавить", "Изменить", "Удалить"]
            for i in arr:
                if rights[index_type] == 2 and table not in rights_attributes[index_type]:
                    continue
                Button(frame_edit, text=i, font=(1, 12),
                       command=lambda i=i: (action(i, table, [i.get() for i in var]),
                                            draw_table(frame_table, get_columns_name(table), "SELECT * FROM " + table + ";"))).pack(
                    side=LEFT,
                    anchor=S, padx=10,
                    pady=10)
            frame_edit.pack(pady=5, fill='x')

        draw_panel(db[0])

        draw_panel(db[0])
    if rights[index_type] == 3:
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
                return ' GROUP BY id_товара'
            else:
                return (' GROUP BY ' + ' and '.join(text))
        """Обявление переменных"""
        padx, pady = 10, 6
        table = rights_attributes[index_type].pop(0)
        columns = list(set(get_columns_name(table)).difference(set(rights_attributes[index_type])))
        renames = [i.split(' - ') for i in connect_bd[10].split(': ')[1].split(', ')]
        for j in range(len(renames)):
            columns = [i.replace(renames[j][0], renames[j][1]) for i in columns]
        mycursor.execute(
            "SELECT CONSTRAINT_NAME, COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME ='товар' AND CONSTRAINT_NAME <>'PRIMARY';")
        text = ''
        for i in mycursor.fetchall():
            text += "LEFT JOIN " + i[0] + " using(" + i[1] + ") "
        text = "SELECT " + ', '.join(columns) + " FROM " + table + " " + text + ";"
        """Окно поиска"""
        frame_search = LabelFrame(window, text='Поиск', font=(1, 15))
        frame_search.pack(side=TOP, anchor=W, padx=20, pady=15)

        search = StringVar()
        Entry(frame_search, textvariable=search).pack(side=LEFT)
        Button(frame_search, text='Поиск', font=(1, 11), command=lambda: draw_table(frame_table, columns, text[:-1] + where(
                                                                                        search, var, var_2, var_3,
                                                                                        arr) + group(var_4[1]) + order(
                                                                                        var_4[0]) + ";")).pack(
            padx=10, side=LEFT)
        """Окно фильтров"""
        frame_filter = LabelFrame(window, text='Фильтры', font=(1, 15), labelanchor=N)  # Окно фильтров
        frame_filter.pack(side=LEFT, anchor=N, padx=20)

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
        """Таблица"""
        frame_table = Frame(window)
        frame_table.pack(side=TOP, anchor=N)

        draw_table(frame_table, columns, text)

    Button(window, text='Выйти', font=(1, 12),
           command=lambda: authorization(type, passwords, rights, rights_attributes)).pack(
        side=BOTTOM, anchor=E)


type = connect_bd[5].split(': ')[1].split(', ')
passwords = connect_bd[6].split(': ')[1].split(', ')
rights = list(map(int, connect_bd[7].split(': ')[1].split(', ')))

rights_attributes = [''] * len(rights)
tables_2 = [i.split(', ') for i in connect_bd[8].split(': ')[1].split('; ')]  # атрибуты для прав 2: доступные таблицы
tables_3 = [i.split(', ') for i in
            connect_bd[9].split(': ')[1].split('; ')]  # атрибуты для прав 3: таблица вывода и колонки исключения

k, l = 0, 0
for i in range(len(rights)):
    if rights[i] == 2:
        rights_attributes[i] = tables_2[k]
        k += 1
    if rights[i] == 3:
        rights_attributes[i] = tables_3[l]
        l += 1

window = Tk()
window.iconbitmap("market.ico")

authorization(type, passwords, rights, rights_attributes)
#work(['Администратор', 'Персонал', 'Клиент'], 2, 'asda', [1, 2, 3], ['', ['продажа'], ['товар']])

window.mainloop()
