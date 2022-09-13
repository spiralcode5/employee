from flask import Flask, render_template, redirect, request, flash, jsonify
import psycopg2
import psycopg2.extras
     
app = Flask(__name__)
     
app.secret_key = "caircocoders-ednalan"
     
DB_HOST = "localhost"
DB_NAME = "restapiDB"
DB_USER = "postgres"
DB_PASS = "postgre"
         
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
     
@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM employee ORDER BY id")
    employee = cur.fetchall()
    return render_template('index.html', employee=employee)
  
@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        txtname = request.form['txtname']
        txtdesignation = request.form['txtdesignation']
        txtaddress = request.form['txtaddress']
        txtphoneno = request.form['txtphoneno']
        print(txtname)
        if txtname == '':
            msg = 'Please Input Name' 
        elif txtdesignation == '':
           msg = 'Please Input Designation' 
        elif txtaddress == '':
           msg = 'Please Input Address'
        elif txtphoneno == '':
           msg = 'Please Input Phone No.' 
        else:        
            cur.execute("INSERT INTO employee (name,designation,address,phoneno) VALUES (%s,%s,%s,%s)",[txtname,txtdesignation,txtaddress,txtphoneno])
            conn.commit()       
            cur.close()
            msg = 'New record created successfully..!'  
    return jsonify(msg)
  
@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        txtname = request.form['txtname']
        txtdesignation = request.form['txtdesignation']
        txtaddress = request.form['txtaddress']
        txtphoneno = request.form['txtphoneno']
        print(string)
        cur.execute("UPDATE employee SET name = %s, designation = %s, address = %s, phoneno = %s WHERE id = %s ", [txtname, txtdesignation, txtaddress,txtphoneno, string])
        conn.commit()       
        cur.close()
        msg = 'Record successfully Updated..!'  
    return jsonify(msg)    
  
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('DELETE FROM employee WHERE id = {0}'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully..!'  
    return jsonify(msg) 
 
if __name__ == "__main__":
    app.run(debug=True)
