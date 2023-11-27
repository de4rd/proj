import tkinter as tk 
from tkinter import ttk
import sqlite3




class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()



    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        

        self.img_add = tk.PhotoImage(file="F:\proj\add.png")
        btn_add = tk.Button(toolbar, text="Добавить", bg="#d7d7d7",
                            bd = 0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)


        self.img_upd = tk.PhotoImage(file="F:\proj\change.png")
        btn_upd = tk.Button(toolbar, bg="#d7d7d7",
                            bd = 0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        self.img_search = tk.PhotoImage(file="F:\proj\search.png")
        btn_search = tk.Button(toolbar, bg="#d7d7d7", 
                               bd = 0, image=self.img_search,
                               command=self.open_searc)
        btn_search.pack(side=tk.LEFT)

        self.img_refresh = tk.PhotoImage(file="F:\proj\refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#d7d7d7",
                                bd = 0, image=self.img_refresh,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)


        self.tree = ttk.Treeview(root,
                                 columns=("id","name","phone","email" ),
                                 height=45,
                                 show="headings")
        
        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        self.tree.heading("id", text="id")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Электронная-Почта")

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    def view_records(self):
        self.db.cur.execute("SELECT * FROM users")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]


    def search_records(self, name):
        self.db.cur.execute("SELECT * FROM users WHERE name LIKE ?",
                            ("%" + name + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute("""
            UPDATE users
            SET name = ?, phone = ?, email = ?
            WHERE id = ?
        """, (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute("DELETE FROM users WHERE id = ?",
                                (self.tree.set(row, "#1"), ))
            
            self.db.conn.commit()
            self.view_records()


    def open_child(self):
        Child()


    def open_update_child(self):
        Update()


    def open_searc(self):
        Search()



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавление контакта")
        self.geometry("600x400")
        self.resizable(False, False)

  

        self.grab_set()


        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)
        label_name = tk.Label(self, text="Телефон")
        label_name.place(x=50, y=80)
        label_name = tk.Label(self, text="E-mail")
        label_name.place(x=50, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=200, y=150)

        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.bind("<Button-1>", lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get()))
        self.btn_add.place(x=265, y=150)


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title("Изменение контакта")
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text="Изменить")
        self.btn_upd.bind("<Button-1>",
                     lambda ev: self.view.update_record(self.entry_name.get(),
                                                        self.entry_phone.get(),
                                                        self.entry_email.get()))
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_upd.place(x=265, y=150)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.db.cur.execute("SELECT * from users WHERE id = ?", (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        self.title("Поиск контакта")
        self.geometry("350x125")
        self.resizable(False, False)

        self.grab_set()

        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=70)

        self.btn_add = tk.Button(self, text="Найти")
        self.btn_add.bind("<Button-1>",
                          lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind("<Button-1>", lambda ev: self.destroy(), add = "+")
        self.btn_add.place(x=225, y=70)
            

class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT
        )""")
        self.conn.commit()

    def insert_data(self, name, phone, email):
        self.cur.execute("""
                         INSERT INTO users (name, phone, email)
                         Values (?, ?, ?)""", (name, phone, email))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()