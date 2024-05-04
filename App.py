from flask import Flask,redirect,render_template,url_for,request,session
from flask_mysqldb import MySQL
import re
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
from flask_bcrypt import check_password_hash

App=Flask(__name__)
App.secret_key="sivapackia"

App.config['MYSQL_HOST']='localhost'
App.config['MYSQL_USER']='root'
App.config['MYSQL_PASSWORD']='Rspk2822@'
App.config['MYSQL_DB']='backend_project'
App.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(App)
bcrypt=Bcrypt(App)

def hash_password_check(password):
    if len(password) <= 5:
        return False
    if not re.search(r"[a-z]",password) or not re.search(r"[A-Z]",password):
        return False
    return True

@App.route("/",methods=["GET","POST"])
def Login():
    if request.method == "POST":
        Email=request.form.get('email')
        Password=request.form.get('password')
        cur=mysql.connection.cursor()
        cur.execute("SELECT id,email,password FROM signup WHERE email=%s",(Email,))
        data=cur.fetchone()
        hash_password=data['password']
        if data and check_password_hash(hash_password,Password):
            return redirect(url_for('Home'))
        cur.connection.commit()
        cur.close()
        
    return render_template("Login.html")

@App.route("/Home")
def Home():
    return render_template("Home.html")



@App.route("/Signup",methods=["GET","POST"])
def Signup():
    if request.method == "POST":
        Email=request.form.get("email")
        Password=request.form.get("password")
        cur=mysql.connection.cursor()
        cur.execute("select *from signup where email=%s",(Email,))
        data=cur.fetchone()
        cur.connection.commit()
        cur.close()
        if data:
            return "Already Email Is Exist"
        else:
            if not hash_password_check(Password):
                return "Check The Password Given Character"
            else:
                hash_password=bcrypt.generate_password_hash(Password).decode('utf-8')
                cur=mysql.connection.cursor()
                cur.execute("insert into Signup (email,password) values(%s,%s)",(Email,hash_password))
                cur.connection.commit()
                cur.close()
                return redirect(url_for('Login'))
    return render_template("Signup.html")
    
@App.route("/Timesheet",methods=["GET","POST"])
def Timesheet():
    if request.method == "POST":
        date=request.form.get("date")
        end_time=request.form.get("end_time")
        start_time=request.form.get("start_time")
        end_time=request.form.get("end_time")
        job_name=request.form.get("job_name")
        job_code=request.form.get("job_code")
        department=request.form.get("department")
        project=request.form.get("project")
        modules=request.form.get("modules")
        session["login_date"]=date
        cur=mysql.connection.cursor()
        cur.execute("insert into timesheet (login_date,start_time,end_time,job_name,job_code,department,project,modules) values(%s,%s,%s,%s,%s,%s,%s,%s)",(date,start_time,end_time,job_name,job_code,department,project,modules))
        cur.connection.commit()
        cur.close()
        return redirect(url_for('Table'))
    
    return render_template("Timesheet.html")

@App.route("/Sheet",methods=["GET","POST"])
def Sheet():
    if request.method == "POST":
        date=request.form.get("date")
        session["login_date"]=date
        return redirect(url_for('Table'))
    return render_template("Sheet.html")

@App.route("/Table",methods=["GET","POST"])
def Table():
    date=session["login_date"]
    cur=mysql.connection.cursor()
    cur.execute("select * from timesheet where login_date=%s",(date,))
    data=cur.fetchall()
    cur.close()
    if request.method == "POST":
        login_date=request.form.get("date")
        session["login_date"]=login_date
        cur=mysql.connection.cursor()
        cur.execute("select * from timesheet where login_date=%s",(login_date,))
        data=cur.fetchall()
        cur.connection.commit()
        cur.close()
        # return redirect(url_for('Table'))
    return render_template("Table.html",data=data)

@App.route("/Delete/<string:id>",methods=["GET","POST"])
def Delete(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from timesheet where id=%s",(id,))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('Table'))

@App.route("/Edit/<string:id>",methods=["GET","POST"])
def Edit(id):
    if request.method=="POST":
        date=request.form.get("date")
        start_time=request.form.get("start_time")
        end_time=request.form.get("end_time")
        job_name=request.form.get("job_name")
        job_code=request.form.get("job_code")
        department=request.form.get("department")
        project=request.form.get("project")
        modules=request.form.get("modules")
        cur=mysql.connection.cursor()
        cur.execute("update timesheet set login_date=%s,start_time=%s,end_time=%s,job_name=%s,job_code=%s,department=%s,project=%s,modules=%s where id=%s",(date,start_time,end_time,job_name,job_code,department,project,modules,id))
        cur.connection.commit()
        cur.close()
        return redirect(url_for('Table'))
    cur=mysql.connection.cursor()
    cur.execute("select *from timesheet where id=%s",(id,))
    data=cur.fetchone()
    cur.connection.commit()
    cur.close()
    return render_template("Edit.html",data=data)


    
if __name__ == ("__main__"):
    App.run(debug=True)