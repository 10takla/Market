import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb

connect_bd = [i.replace('\n', '') for i in open("host_connect.txt", encoding='utf-8')]


def search_file(word):
    for i in connect_bd:
        if word in i:
            i = i.split(': ', 1)[1]
            if '; ' in i:
                i = i.split('; ')
                for l in i:
                    if ', ' in l:
                        i[i.index(l)] = l.split(', ')
                        for k in i:
                            for j in k:
                                if ' - ' in j:
                                    i[i.index(k)][k.index(j)] = j.split(' - ')
                    elif ' - ' in l:
                        i[i.index(l)] = l.split(' - ')
            if ', ' in i:
                i = i.split(', ')
                for j in i:
                    if ' - ' in j:
                        i[i.index(j)] = j.split(' - ')

            if ' - ' in i:
                i = i.split(' - ')
            return i


mydb = mysql.connector.connect(
    host=search_file('host'),
    user=search_file('user'),
    password=search_file('password'),
    database=search_file('database')
)
mycursor = mydb.cursor()


class Filters(LabelFrame):
    def __init__(self, frame_filter=None, text=''):
        self.frame_filter = frame_filter
        self.text = text
        self.frame_widgets = LabelFrame(self.frame_filter, text=self.text.title(), font=(1, 13))
        self.frame_widgets.pack(anchor=W, padx=10, pady=6)

    def having(self, arr):
        var = []
        k = [i.replace('_', ' ') for i in [arr, "Не " + arr]]
        for i in range(len(k)):
            var += [IntVar()]
            Checkbutton(self.frame_widgets, text=k[i].title(), variable=var[i], onvalue=1, offvalue=0).pack(
                anchor=W)
        return var

    def diapazon(self, increment):
        array = ['От', 'До']
        var = []
        for i in array:
            Label(self.frame_widgets, text=i).pack(side=LEFT)
            var += [IntVar()]
            Spinbox(self.frame_widgets, from_=0, to=increment * 1000, increment=increment, width=7,
                    textvariable=var[array.index(i)]).pack(
                side=LEFT)
        return var

    def selected(self, table, join_table):
        mycursor.execute("SELECT " + self.text + " FROM " + table + " " + join_table + ";")
        l = list(set(i for j in mycursor.fetchall() for i in j))
        var = []
        for i in l:
            var += [StringVar()]
            Checkbutton(self.frame_widgets, text=i, variable=var[l.index(i)], onvalue=i, offvalue='').pack(anchor=W)
        return var

    def sort(self, arr_5):
        var = StringVar()
        ttk.Combobox(self.frame_widgets, textvariable=var, values=arr_5).pack()
        return var

    def grot(where, order, group):
        where = [[j.get() for j in i] for i in where]
        order = [i.get() for i in order]
        group = [i.get() for i in group]
        print(where, order, group)


class SQL():
    def where(self, search, having, between, where):
        having = [i.get() for i in having]
        between = [i.get() for i in between]
        where = [[j.get() for j in i] for i in where]

        text = 'WHERE ' + search_file('Поиск') + ' LIKE "_%' + search.get() + '_%"'

        if having[0] == 1 and having[1] == 0:
            text += " AND в_наличии != '0'"
        elif having[0] == 0 and having[1] == 1:
            text += " AND в_наличии = '0'"

        if between[0] < between[1]:
            text += " AND цена BETWEEN " + str(between[0]) + " and " + str(between[1])

        for i in range(len(where)):
            g = list(filter(None, where[i]))
            g = [f'"{i}"' for i in g]
            if len(g) != 0:
                text += ' AND ' + search_file('Таблицы для фильтров')[i] + " IN ({})".format(', '.join(g))

        return text

    def order(self, var_4):
        text = []
        if var_4.get() == 'Сначала дорогие':
            text += ["цена DESC"]
        elif var_4.get() == 'Сначала дешевые':
            text += ["цена ASC"]
        if len(text) == 0:
            return ''
        else:
            return (' ORDER BY ' + ' and '.join(text))

    def group(self, var_4):
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
    print(text)
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
        elif (rights[index_type] == 1 or rights[index_type] == 2) and log_pass[1] != passwords[index_type]:
            mb.showerror("Ошибка", "Неправильный логин или пароль!")
        else:
            work(type, index_type, log_pass[0], rights, rights_attributes)


def work(type, index_type, login, rights, rights_attributes):
    destroy(window)
    window.title(type[index_type] + ' ' + login)
    window.minsize(200, 210)
    if rights[index_type] in [1, 2]:

        mycursor.execute("SHOW TABLES FROM " + search_file('магазин') + ";")
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
                                            draw_table(frame_table, get_columns_name(table),
                                                       "SELECT * FROM " + table + ";"))).pack(
                    side=LEFT,
                    anchor=S, padx=10,
                    pady=10)
            frame_edit.pack(pady=5, fill='x')

        draw_panel(db[0])

        draw_panel(db[0])
    if rights[index_type] == 3:
        """Обявление переменных"""
        table = rights_attributes[index_type].pop(0)
        columns = list(set(get_columns_name(table)).difference(set(rights_attributes[index_type])))
        renames = search_file('Замена колонок')
        for j in range(len(renames)):
            columns = [i.replace(renames[j][0], renames[j][1]) for i in columns]
        mycursor.execute(
            "SELECT CONSTRAINT_NAME, COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME ='товар' AND CONSTRAINT_NAME <>'PRIMARY';")
        join_table = ''
        for i in mycursor.fetchall():
            join_table += "LEFT JOIN " + i[0] + " using(" + i[1] + ") "
        text = "SELECT " + ', '.join(columns) + " FROM " + table + " " + join_table + ";"

        """Окно поиска"""
        frame_search = LabelFrame(window, text='Поиск', font=(1, 15))
        frame_search.pack(side=TOP, anchor=W, padx=20, pady=15)

        search = StringVar()
        Entry(frame_search, textvariable=search).pack(side=LEFT)
        Button(frame_search, text='Поиск', font=(1, 11),
               command=lambda: draw_table(frame_table, columns,
                                          text[:-1] + SQL().where(search, having, between, where) + SQL().group(
                                              group) + SQL().order(
                                              order) + ";")).pack(
            padx=10, side=LEFT)

        """Окно фильтров"""
        frame_filter = LabelFrame(window, text='Фильтры', font=(1, 15), labelanchor=N)  # Окно фильтров
        frame_filter.pack(side=LEFT, anchor=N, padx=20)

        having = Filters(frame_filter).having(search_file('Having'))
        t = search_file('BETWEEN')
        between = Filters(frame_filter, t[0].title()).diapazon(int(t[1]))
        where = []
        for i in search_file('Таблицы для фильтров'):
            where += [Filters(frame_filter, i).selected(table, join_table)]
        order = Filters(frame_filter, 'Соритровка').sort(search_file('Сортировка'))
        group = Filters(frame_filter, 'Группировка').sort(search_file('Группировка'))
        Button(frame_search, text='Поиск', font=(1, 11),
               command=lambda: SQL().order(order)).pack(padx=10, side=LEFT)

        """Таблица"""
        frame_table = Frame(window)
        frame_table.pack(side=TOP, anchor=N)

        draw_table(frame_table, columns, text)

    Button(window, text='Выйти', font=(1, 12),
           command=lambda: authorization(type, passwords, rights, rights_attributes)).pack(
        side=BOTTOM, anchor=E)


type = search_file('Типы пользователей')
passwords = search_file('Пароли')
rights = list(map(int, search_file('Права')))

rights_attributes = [''] * len(rights)
tables_2 = search_file('Атрибуты права 2')  # атрибуты для прав 2: доступные таблицы
tables_3 = search_file('Атрибуты права 3')  # атрибуты для прав 3: таблица вывода и колонки исключения
k, l = 0, 0
for i in range(len(rights)):
    if rights[i] == 2:
        rights_attributes[i] = tables_2
        k += 1
    if rights[i] == 3:
        rights_attributes[i] = tables_3
        l += 1
window = Tk()
window.iconbitmap("market.ico")

# authorization(type, passwords, rights, rights_attributes)
work(['Администратор', 'Персонал', 'Клиент'], 2, 'asda', [1, 2, 3], ['', 'продажа', ['товар', 'id_поставки']])

window.mainloop()
