from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import time
import pizza_back

#creating database if doesn't exist
with sqlite3.connect('pizza.db') as db:
    c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL ,password TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS user_orders (username TEXT NOT NULL, pizza_id  TEXT NOT NULL,price INT);')
db.commit()
db.close()

class main:
    def __init__(self,entryscreen):
        #main screen configuration
        self.entryscreen = entryscreen
        self.entryscreen.title("TarlaPizza")
        self.entryscreen.geometry("700x700")
        self.entryscreen.configure(bg="turquoise")

        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()

        self.widgets()
    #login function
    def login(self):
        with sqlite3.connect('pizza.db') as db:
            c = db.cursor()

        find_user = ('SELECT * FROM users WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        #admin's username and password
        if self.username.get()=="admin" and self.password.get()=="admin":
            self.logf.pack_forget()
            self.admin_b_seeorders.place(x=100,y=150)
            self.admin_b_income.place(x=350,y=150)

        elif result:
            self.logf.pack_forget()
            self.label_main.place(x=25,y=100)
            self.label2_main.place(x=380,y=100)
            self.p1.place(x=200,y=290)
            self.p2.place(x=380,y=290)
            self.l1.place(x=240,y=350)
            self.b1.place(x=180,y=400)
            self.b2.place(x=370,y=400)
            self.label_extention.place(x=250,y=450)
            self.b_tomato.place(x=170,y=490)
            self.b_cheese.place(x=420,y=490)
            self.b_mushroom.place(x=280,y=490)
            self.b_order.place(x=290,y=550)
            self.b_prev.place(x=230,y=600)

        else:
            ms.showerror('Not found','Username Not Found!')

    #to check admin's income
    def admin_income(self):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        result = [x[0] for x in c.execute("SELECT price FROM user_orders")]
        count=0
        for i in result:
            count+=i
        string="Your income is "+str(count)+" dollars"
        self.admin_l1=Label(self.entryscreen,text=string,bg='lawn green',font=("arial",20))
        self.admin_l1.place(x=170,y=250)

    #to see all orders
    def admin_orders(self):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        result1=[x[0] for x in c.execute('SELECT username FROM user_orders')]
        result2=[x[0] for x in c.execute('SELECT pizza_id FROM user_orders')]

        for i in range(len(result1)):
            print(result1[i],result2[i])

    #pizza creator function
    def create_pizza(self,a):
        if a=="Pepperoni":
            self.pizza=pizza_back.PizzaBuilder(a)
        elif a=="Barbeque":
            self.pizza=pizza_back.PizzaBuilder(a)

    #add extensions to the pizza
    def add_remove(self,pizza_type,extention,choice):
        if choice=="add":
            self.pizza.add_extention(extention)
        elif choice=="remove":
            self.pizza.remove_extention(extention)

    #see order's total price
    def order_price(self,pizza):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        insert='INSERT INTO user_orders(username,pizza_id,price) VALUES(?,?,?)'
        c.execute(insert,[(self.username.get()),(self.pizza.get_status()),(self.pizza.get_price())])
        db.commit()
        ms.showinfo('Price','Your order {} is {} dollars'.format(self.pizza.get_status(),self.pizza.get_price()))

    #see previous orders' list
    def previous_order(self):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        find_user=('SELECT * FROM user_orders WHERE username=?')
        c.execute(find_user,[(self.username.get())])
        result=c.fetchall()
        print("Username is",result[0][0])
        for i in result:
            print("Order:",i[1],end="|")
            print("Price:",i[2],"dollar")

    #register function
    def register_user(self):
        username_info = username.get()
        password_info = password.get()
        password2_info = password2.get()

        register_parameters=(username_info,password_info)
        with sqlite3.connect('pizza.db') as db:
            c = db.cursor()
        c.execute("SELECT username FROM users WHERE username=?",(username_info,))
        result=c.fetchall()
        if username_info=="":
            ms.showerror("Error","Enter username!")
        elif len(result)>0:
          ms.showerror("Username already taken!","Try another username!")
        else:
          if password_info!=password2_info:
            ms.showerror("Error","Passwords don't match!")
            password_entry1.delete(0, END)
            password_entry2.delete(0, END)
          elif password_info==password2_info:
              c.execute("INSERT INTO users VALUES ( ?, ? )", register_parameters)
              db.commit()
              username_entry.delete(0, END)
              password_entry1.delete(0, END)
              password_entry2.delete(0, END)
              Label(regscreen, text = "Successfully registered!",bg ='light cyan', fg = "green" ,font = ("calibri", 10, 'bold')).pack()

    #create account interface
    def create(self):
        global regscreen
        regscreen=Toplevel(self.entryscreen)
        regscreen.title("Registery page")
        regscreen.geometry("350x300")

        global username
        global password
        global password2
        global username_entry
        global password_entry1
        global password_entry2
        username = StringVar()
        password = StringVar()
        password2 = StringVar()
        regscreen.configure(bg="dark turquoise")
        Label(regscreen, text = "Please enter details:",bg='dark turquoise', font=("Times",14,"bold")).pack()
        Label(regscreen, text = "",bg='dark turquoise').pack()
        #username/password1/password2
        Label(regscreen, text = "Username:",bg='dark turquoise').pack()
        username_entry = Entry(regscreen, textvariable = username)
        username_entry.pack()
        Label(regscreen, text = "Password:",bg='dark turquoise').pack()
        password_entry1 =  Entry(regscreen, textvariable = password)
        password_entry1.pack()
        Label(regscreen, text = "Repeat password:",bg='dark turquoise').pack()
        password_entry2 =  Entry(regscreen, textvariable = password2)
        password_entry2.pack()
        Label(regscreen, text = "",bg='dark turquoise').pack()
        Button(regscreen, text = "Register", width = 10, height = 1, command = self.register_user).pack()

    #widgets interface
    def widgets(self):
        Label(self.entryscreen,text = 'Welcome to TarlaPizza!',bg = "yellow", width = "35", height = "3", font = ("Calibri", 17, 'bold')).pack()
        self.logf = Frame(self.entryscreen,bg='turquoise')
        self.logf.pack()
        Label(self.logf, text = "Log in to get pizza :)", bg = "orange", width = "20", height = "1", font = ("Calibri", 15)).pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf, text = "Username: ",bg='turquoise',font=('Times',20),width='16',height='1').pack()
        Entry(self.logf,width='24', textvariable = self.username).pack()
        Label(self.logf, text = "Password: ",bg='turquoise',font=('Times',20),width='16',height='1').pack()
        Entry(self.logf,width='24', textvariable = self.password).pack()
        Button(self.logf,text = ' Login ',width = 8, font = ('',12,), height = 1,command=self.login).pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf, text = "Not registered yet?",bg='gold',font=('Times',13),width='15',height='1').pack()
        Button(self.logf,text = ' Create Account ',font = ('',12),command=self.create).pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf,text = '', bg="turquoise").pack()
        Label(self.logf, text = "[Here could be your advertisement]",bg='orange',font=('Times',11),width='30',height='1').pack()

        self.label_main=Label(self.entryscreen)
        self.label_main.img=ImageTk.PhotoImage(file="pizza2.jpg")
        self.label_main.config(image=self.label_main.img)
        self.label_main.pack_forget()

        self.label2_main=Label(self.entryscreen)
        self.label2_main.img=ImageTk.PhotoImage(file="pizza1.jpg")
        self.label2_main.config(image=self.label2_main.img)
        self.label2_main.pack_forget()

        self.p1=Label(self.entryscreen,text="Pepperoni",font=("arial",17,'bold'),bg="orange")
        self.p1.pack_forget()
        self.p2=Label(self.entryscreen,text="Barbeque",font=("arial",17,'bold'),bg="orange")
        self.p2.pack_forget()
        self.l1=Label(self.entryscreen,text="Choose your order:",font=("Times",20),bg="lawn green")
        self.l1.pack_forget()

        self.v=IntVar()
        self.b1=Radiobutton(self.entryscreen,variable=self.v,value=1,bg='pink1',text="PEPPERONI",font=('',15),command=lambda:self.create_pizza("Pepperoni"))
        self.b2=Radiobutton(self.entryscreen,variable=self.v,value=2,bg='pink1',text="BARBECUE",font=('',15),command=lambda:self.create_pizza("Barbeque"))
        self.b1.pack_forget()
        self.b2.pack_forget()
        self.label_extention=Label(self.entryscreen,text="Add extentions:",bg='green yellow',font=("arial",20))
        self.label_extention.pack_forget()
        self.b_tomato=Button(self.entryscreen,text="Tomato",bg='brown1',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Tomato","add"))
        self.b_tomato.pack_forget()
        self.b_cheese=Button(self.entryscreen,text="Cheese",bg='khaki',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Cheese","add"))
        self.b_cheese.pack_forget()
        self.b_mushroom=Button(self.entryscreen,text="Mushroom",bg='lemon chiffon',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Mushroom","add"))
        self.b_mushroom.pack_forget()
        self.b_order=Button(self.entryscreen,text="ORDER",bg='green3',bd=3,font=('',15),command=lambda:self.order_price(self.pizza))
        self.b_order.pack_forget()
        self.b_prev=Button(self.entryscreen,text="See previous orders",bg='azure2',bd=3,font=('',15),command=lambda:self.previous_order())
        self.b_prev.pack_forget()

        self.admin_b_seeorders=Button(self.entryscreen,text="See all orders",bd=3,font=('arial',20),bg="gold",command=lambda:self.admin_orders())
        self.admin_b_seeorders.pack_forget()
        self.admin_b_income=Button(self.entryscreen,text="See your income",bd=3,font=('arial',20),bg="gold",command=lambda:self.admin_income())
        self.admin_b_income.pack_forget()

root = Tk()
root.geometry("1000x1000")

main(root)
root.mainloop()
