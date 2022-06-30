from sqlite3 import connect
import sqlite3
import datetime

# ------------------------  Check User qismi -----------------
def create_table():
    conn  = sqlite3.connect("main.db")
    cursor  = conn.cursor()
    cursor.execute("""
    Create Table IF Not Exists humans(
    id Integer Primary Key Unique,
    telegram_id Integer,
    full_name Varchar(125) ,
    first_name Varchar(125),
    phone Varchar(30),
    viloyat Varchar(120)   
    )
    """)
    conn.commit()


def insert_table(telegram_id,full_name,first_name,phone,viloyat):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Insert Into humans(telegram_id,full_name,first_name,phone,viloyat)
    Values ({telegram_id},"{full_name}", "{first_name}","{phone}","{viloyat}")
    """)
    conn.commit()



def check_user(telegram_id):
    conn = connect('main.db')
    cursor = conn.cursor()


    cursor.execute(f"""
    select * from humans
    where telegram_id = {telegram_id}
    
    """)

    data = cursor.fetchone()
    if data:
        return True

    else:
        return False


##### --------------------Kitob qismlari --------------------- ####

def books_category():
    conn  = sqlite3.connect("main.db")
    cursor  = conn.cursor()
    cursor.execute("""
    Create Table IF Not Exists books(
    id Integer Primary Key Unique,
    name Varchar(120)
    )
    """)
    conn.commit()

books_category()

def books_category_select():
    conn = connect('main.db')
    cursor = conn.cursor()
    
    cursor.execute(f"""
    select * from books

    """)

    data = cursor.fetchall()
    return data

books_category_select()

def books_name():
    conn = connect('main.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    Create Table If Not Exists books_name(
    id Integer Primary Key Unique,
    cat_id Integer,
    book_name Varchar(120),
    price Integer,
    image Varchar(150)
    )
    """)
    conn.commit()
books_name()

    
def get_books_by_cat_id(cat_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from books_name
    where cat_id = {cat_id}
    """)
    data = cursor.fetchall()
    return data


    
def get_books_name_catid(cat_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from books
    where id = {cat_id}
    """)
    data = cursor.fetchall()
    return data

# print(get_books_name_catid(1))


def get_book(book_id):
    conn = connect('main.db')
    cursor = conn.cursor()


    cursor.execute(f"""
    select * from books_name
    where id = {book_id}
    
    """)

    data = cursor.fetchone()
    return data



def orders_table():
    conn = connect('main.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    Create Table If Not Exists Orders(
    ord_id Integer Primary Key Unique,
    user_id Integer,
    order_date datetime,
    status Varchar(120) default 'progress')
    """)
    conn.commit()

orders_table()


def  get_order(telegram_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    
    cursor.execute(f"""
    select * from Orders
    where user_id = (select id from humans
    where telegram_id = {telegram_id}) and status = "progress"
    """)
    data = cursor.fetchone()
    if not(data):
        cursor.execute(f"""
        Insert Into Orders(user_id)
        values ((select id from humans
        where telegram_id = {telegram_id})

        )
        """)
        conn.commit()
        cursor.execute(f"""
        select * from Orders
        where user_id = (select id from humans
        where telegram_id = {telegram_id}) and status = "progress"
        """)
        data = cursor.fetchone()
        return data[0]
       

    else:
        return data[0]

# print(get_order(1306354017))
def orders_table_details():
    conn = connect('main.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    Create Table If Not Exists order_table(
    id Integer Primary Key Unique,
    order_id Integer,
    product_id Integer,
    quantity Integer,
    tg_id Integer
    )
    """)
    conn.commit()

orders_table_details()

def add_order_table(order_id,product_id,quantity,tg_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from order_table
    where order_id = "{order_id}"  and product_id = "{product_id}"
    """)
    data = cursor.fetchall()
    if not data:
        cursor.execute(f"""
        Insert Into order_table(order_id,product_id,quantity,tg_id)
        Values ("{order_id}", "{product_id}", "{quantity}","{tg_id}")
        """)
        conn.commit()
    else:
        cursor.execute(f"""
        Update order_table
        Set quantity = quantity+"{quantity}"
        where order_id = "{order_id}"  and product_id = "{product_id}"
        """)
        conn.commit()
    



def add_category(cat_name):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Insert into books (name)
    values ("{cat_name}")
    """)
   
    conn.commit()


def add_product_by_id(cat_id,name,price):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Insert Into books_name (cat_id,book_name,price)
    values ({cat_id},"{name}",{price})
    """)
    conn.commit()
    



def get_order_books(order_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from order_table
    where order_id = "{order_id}"

    """)
    data = cursor.fetchall()
    return data



def get_books(cat_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from books_name
    where id = "{cat_id}"

    """)
    data = cursor.fetchone()
    return data

def update_order_det(id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Update order_table
    Set  quantity=quantity+1
    where id={id}
    """)
    conn.commit()

def update_order_detail(id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Update order_table
    Set  quantity=quantity-1
    where id={id}
    """)
    conn.commit()



def check_ord_det(id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select quantity from order_table
    where id = {id}
    """)
    data = cursor.fetchone()[0]
    if data ==1:
        cursor.execute(f"""
        Delete from order_table
        where id = {id}
        """)
        conn.commit()
        return False

    else:
        return True






def change_order_status(order_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute(f"""
    Update Orders
    Set status = 'done' , order_date = Current_TimeStamp
    where ord_id="{order_id}"
    """)
    conn.commit()




def get_humans(telegram_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Select * from humans
    where telegram_id={telegram_id}
    """)
    data  = cursor.fetchall()
    return data


def get_order_confirm(telegram_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from Orders
    where user_id = (select id from humans
                    where telegram_id = {telegram_id}) and status = "progress"
    """)
    data = cursor.fetchone()
    return data


def get_done_status(telegram_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from Orders
    where user_id = (select id from humans
                    where telegram_id = {telegram_id}) and status = "done"
    """)
    data = cursor.fetchall()
    return data
       


def delete_orders(telegram_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Delete from order_table
    where tg_id = {telegram_id}
    """)
    conn.commit()

def del_done_status(telegram_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    Delete from Orders
    where user_id = (select id from humans
                    where telegram_id = {telegram_id}) and status = "done"
    """)
    conn.commit()


def get_humans_all():
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from humans
    """)
    data = cursor.fetchall()
    return data

