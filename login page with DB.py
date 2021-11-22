from flask import Flask,render_template,request,redirect
import pymysql,re
loginpage=Flask(__name__) #app=Flask(__name__)
con=None
cursor=None

def connectDb():
    global con,cursor
    con=pymysql.connect(host='localhost',user='root',password='root',database='logininfo')
    cursor=con.cursor()

def closeDb():
    cursor.close()
    con.close()

@loginpage.route('/')
def index():
    return render_template('index.html')



@loginpage.route('/Register',methods=['GET','POST'])
def Register():
    msg=''
    if request.method=='POST':
        value=request.form
        ID=value['id']
        NAME=value['name']
        EMAIL=value['email_id']
        MOBILENO=value['mobileNo']
        PASSWORD=value['password']
        ADDRESS=value['address']
        connectDb()
        cursor.execute("select * from DATA where ID ={}".format(ID))
        status=cursor.fetchone()
        if status:
            msg = '**Account Id already exists**!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',EMAIL):
            msg = 'Invalid email address !'
        elif not ID or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form !'
        elif not re.match(r'^[7-9]\d{9}', MOBILENO):
            msg = 'Enter correct mobile number !'
        else:
            insertdata(ID,NAME,EMAIL,MOBILENO,PASSWORD,ADDRESS)

            msg = 'You have successfully registered !'
            print('data inserted')


    return render_template('register.html',msg=msg)

def insertdata(id,name,email_id,mobileNo,password,address):
    try:
        connectDb()
        query = "insert into DATA values({},'{}','{}',{},'{}','{}');".format(id,name,email_id,mobileNo,password,address)
        cursor.execute(query)
        con.commit()
        print('Registred successfully')
        return True
    except pymysql.DatabaseError:
        return False
        closeDb()
    #login()

@loginpage.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        id =(request.form['id'])
        password =(request.form['password'])
        connectDb()
        query =("select * from data where id={};".format(id))
        cursor.execute(query)
        global data,l
        data=cursor.fetchone()


        l=data
        if data!=None:
            if data[0] == int(id):
                if data[4] == str(password):
                    msg = 'Looged In....'
                    return redirect('http://127.0.0.1:5000/list')
                else:
                    msg = 'inccorect password'
                    return render_template('login.html', msg=msg)
        else:
            msg = 'id dose not matched'
            closeDb()
            return render_template('login.html', msg=msg)
    return render_template('login.html',msg=msg)
@loginpage.route('/list')
def list():
    try:
        data=l
        msg = 'Looged in'
    except NameError:
        msg = '**Login First!'
        return render_template('login.html',msg=msg,)
    return render_template('product.html', msg=msg, data=data)

@loginpage.route('/music',methods=['GET','POST'])
def music():
    msg='Enjoy Music'
    return render_template('hindi.html', msg=msg)
@loginpage.route('/marathi',methods=['GET','POST'])
def marathi():
    msg='Enjoy Music'
    return render_template('marathi.html', msg=msg)
@loginpage.route('/logout',methods=['GET','POST'])
def logout():
    msg='Logged out succesfully!'
    l=data=0
    return render_template('index.html',msg=msg,data=l)




loginpage.run(debug=True)