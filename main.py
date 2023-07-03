from flask import Flask, jsonify, request, render_template, redirect
import mysql.connector
import pandas as pd
from mysql.connector import connect, Error


def send_view_query(connection, query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result, True
    except Error as e:
        print(e)
        return e, False


def send_modifying_query(connection, query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        print(e)
        return e



app = Flask(__name__)

# Database configuration
DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': 'new_password',
    'database': 'industrial_internships3'
}

conn = mysql.connector.connect(**DATABASE)
# Helper function to establish a database connection
def get_db():
    conn = mysql.connector.connect(**DATABASE)
    return conn


@app.route('/')
def index():
    return render_template('index.html')

# Route to retrieve all students from the database
@app.route('/students', methods=['POST'])
def get_students():
    result, e = send_view_query(conn, 'SELECT * FROM student;')
    if e is not True:
        return

    table = pd.DataFrame(result)
    table.columns = ("name", "surname",  "login", "email", "phone", "personal_information", "education_details")
    html_table = table.to_html()
    return render_template("with_output.html", output=html_table)

@app.route('/add-student', methods=['POST'])
def add_student():
    student_data = request.form

    # Extract the student details from the request data
    name = student_data.get('name')
    surname = student_data.get('surname')
    login = student_data.get('login')
    email = student_data.get('email')
    phone = student_data.get('phoneNumber')
    personal_information = student_data.get('personal_information')
    education_details = student_data.get('education_details')

    response = send_modifying_query(conn, f"INSERT INTO student (name, surname, login, email, phone,\
     personal_information, education_details) VALUES ('{name}', '{surname}', '{login}', '{email}', \
     '{phone}', '{personal_information}', '{education_details}');")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/delete-student', methods=['POST'])
def del_student():
    student_data = request.form

    login = student_data.get('login')
    response = send_modifying_query(conn, f"DELETE FROM student WHERE login = '{login}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/modify-student', methods=['POST'])
def modify_student():
    student_data = request.form

    # Extract the student details from the request data
    name = student_data.get('name')
    surname = student_data.get('surname')
    login = student_data.get('login')
    email = student_data.get('email')
    phone = student_data.get('phoneNumber')
    personal_information = student_data.get('personal_information')
    education_details = student_data.get('education_details')
    response = send_modifying_query(conn, f"UPDATE student SET name = '{name}', surname = '{surname}', email = '{email}', phone = '{phone}', personal_information = '{personal_information}', education_details = '{education_details}' WHERE login = '{login}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/companies', methods=['POST'])
def get_companies():
    result, e = send_view_query(conn, 'SELECT * FROM company;')
    if e is not True:
        return

    table = pd.DataFrame(result)
    table.columns = ("id", "name","town", "address", "email")
    html_table = table.to_html()
    return render_template("with_output.html", output=html_table)

@app.route('/add-company', methods=['POST'])
def add_company():
    company_data = request.form

    # Extract the student details from the request data
    name = company_data.get('name')
    town = company_data.get('town')
    address = company_data.get('address')
    email = company_data.get('email')

    response = send_modifying_query(conn, f"INSERT INTO company (name, town, address, email) VALUES ('{name}', '{town}', '{address}','{email}');")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/delete-company', methods=['POST'])
def del_company():
    company_data = request.form

    id = company_data.get('id')
    response = send_modifying_query(conn, f"DELETE FROM company WHERE id = '{id}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/modify-company', methods=['POST'])
def modify_company():
    company_data = request.form
    id = company_data.get("id")
    name = company_data.get('name')
    town = company_data.get('town')
    address = company_data.get('address')
    email = company_data.get('email')
    response = send_modifying_query(conn, f"UPDATE company SET name = '{name}', town = '{town}',  address = '{address}', email = '{email}' WHERE id = '{id}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/internships', methods=['POST'])
def get_internships():
    result, e = send_view_query(conn, 'SELECT * FROM internship;')
    if e is not True:
        return

    table = pd.DataFrame(result)
    table.columns = ("id", "title","description", "start", "end", "company")
    html_table = table.to_html()
    return render_template("with_output.html", output=html_table)

@app.route('/add-internship', methods=['POST'])
def add_internship():
    internship_data = request.form

    # Extract the student details from the request data
    title = internship_data.get('title')
    description = internship_data.get('description')
    start = internship_data.get('start')
    end = internship_data.get('end')
    company = int(internship_data.get('company'))

    response = send_modifying_query(conn, f"INSERT INTO internship (title, description, start, end, company) VALUES ('{title}', '{description}', '{start}','{end}', '{company}');")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/delete-internship', methods=['POST'])
def del_internship():
    internship_data = request.form

    id = internship_data.get('id')
    response = send_modifying_query(conn, f"DELETE FROM internship WHERE id = '{id}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/applications', methods=['POST'])
def get_applications():
    result, e = send_view_query(conn, 'SELECT * FROM application;')
    if e is not True:
        return

    table = pd.DataFrame(result)
    table.columns = ("student", "submitted","internship", "feedback", "motivation_letter", "projects")
    html_table = table.to_html()
    return render_template("with_output.html", output=html_table)

@app.route('/add-application', methods=['POST'])
def add_application():
    application_data = request.form

    # Extract the student details from the request data
    student = application_data.get('student')
    submitted = application_data.get('submitted')
    internship = application_data.get('internship')
    motivation_letter = application_data.get('motivation_letter')
    projects = application_data.get('projects')

    response = send_modifying_query(conn, f"INSERT INTO application (student, submitted, internship, motivation_letter, projects) VALUES ('{student}', '{submitted}', '{internship}','{motivation_letter}', '{projects}');")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")

@app.route('/delete-application', methods=['POST'])
def del_application():
    application_data = request.form

    student = application_data.get('student')
    internship = application_data.get('internship')
    response = send_modifying_query(conn, f"DELETE FROM application WHERE student = '{student}' AND internship = '{internship}';")
    if response is not True:
        print(response)
        return render_template("with_output.html", error=response)

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
