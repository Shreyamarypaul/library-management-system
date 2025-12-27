import mysql.connector
from datetime import datetime,timedelta
db=mysql.connector.connect(host="localhost",user="root",password="my_password")
cursor=db.cursor()
cursor.execute("create database if not exists library_db")
cursor.execute("use library_db")
cursor.execute("""
create table if not exists books(
  book_id int primary key auto_increment,
  title varchar(100),
  author varchar(100),
  quantity int
)
""")
cursor.execute("""
create table if not exists users(
  user_id int primary key auto_increment,
  name varchar(100)
  )
  """)
cursor.execute("""
create table if not exists issued_books(
  issue_id int primary key auto_increment,
  book_id int,
  user_id int,
  issue_date date,
  due_date  date,
  return_date date,
  fine int
)
""")
db.commit()

def add_book():
  title=input("enter book title")
  author=input("enter book author")
  qty=int(input("enter quantity"))
  cursor.execute("insert into books(title,author,quantity)values(%s,%s,%s)",(title,author,qty))
  db.commit()
  print("book added")
  
def view_books():
  cursor.execute("select * from books")
  books=cursor.fetchall()
  print("\n{:<8} {:<30}{:<25}{:<10}".format("ID","Title","Author","Quantity"))
  print("-"*75)
  for i in books:
    
    print("\n{:<8} {:<30}{:<25}{:<10}".format(i[0],i[1],i[2],i[3]))
def add_user():
  name=input("enter user name")
  cursor.execute("insert into users(name)values(%s)",(name,))
  db.commit()
  print("user added")
  
def issue_book():
  book_id=int(input("enter book id"))
  user_id=int(input("enter user id"))
  cursor.execute("select quantity from books where book_id=%s",(book_id,))
  result=cursor.fetchone()
  if result and result[0]>0:
    issue_date=datetime.today().date()
    due_date=issue_date+timedelta(days=7)
    cursor.execute("insert into issued_books(book_id,user_id,issue_date,due_date,return_date,fine)values(%s,%s,%s,%s,NULL,0)",(book_id,user_id,issue_date,due_date))
    cursor.execute("update books set quantity = quantity-1 where book_id=%s",(book_id,))
    db.commit()
    print("book issued")
  else:
    print("book not available")
	
def return_book():
  issue_id=int(input("enter issue id"))
  cursor.execute("select due_date,book_id from issued_books where issue_id=%s",(issue_id,))
  data=cursor.fetchone()
  if data:
      
    due_date=data[0]
    return_date=datetime.today().date()
    late_days=(return_date-due_date).days
    if late_days>0:
      fine=late_days*5
    else:
      fine=0
    cursor.execute("update issued_books set return_date=%s,fine=%s where issue_id=%s",(return_date,fine,issue_id))
    cursor.execute("update books set quantity=quantity+1 where book_id=%s",(data[1],))
    db.commit()
    print("book returned")
    print("fine=",fine)
  else:
    print("invalid issue id")

def menu():
  while True:
    print("""
	LIBRARY MANAGEMENT SYSTEM:
	1.Add book
	2.View books
	3.Add user
	4.Issue book
	5.Return book
	6.Exit
	""")
    choice=input("enter choice")
    if choice=='1':
      add_book()
    elif choice=='2':
      view_books()
    elif choice=='3':
      add_user()
    elif choice=='4':
      issue_book()
    elif choice=='5':
      return_book()
    elif choice=='6':
      print("thank you")
      break
    else:
      print("invalid choice")
menu()
db.close()	  
	
  
