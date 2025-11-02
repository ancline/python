import sys
sys.path.insert(0, "db/")
from dbhelper import *
from flask import Flask, render_template, request, redirect, url_for
from sqlite3 import connect

app = Flask(__name__)

# --- Display students ---
@app.route("/")
def index():
    students = getall("students")
    return render_template("index.html", studentlist=students, student=None)


# --- Add student ---
@app.route("/add", methods=["POST"])
def add_student():
    lastname = request.form.get("lastname", "").strip()
    firstname = request.form.get("firstname", "").strip()
    course = request.form.get("course", "")
    level = request.form.get("level", "")

    if lastname and firstname:
        try:
            conn = connect('db/school.db')
            cursor = conn.cursor()
            
            # Get the max idno and add 1
            cursor.execute("SELECT MAX(CAST(idno AS INTEGER)) FROM students")
            result = cursor.fetchone()
            max_idno = result[0] if result[0] else 1000
            new_idno = str(max_idno + 1)
            
            # Insert with auto-generated idno
            cursor.execute("""
                INSERT INTO students (idno, lastname, firstname, course, level)
                VALUES (?, ?, ?, ?, ?)
            """, [new_idno, lastname, firstname, course, level])
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Add error: {e}")
            
    return redirect(url_for("index"))


# --- Delete student ---
@app.route("/delete/<idno>")
def delete_student(idno):
    try:
        conn = connect('db/school.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE idno = ?", [idno])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Delete error: {e}")
    return redirect(url_for("index"))


# --- Show edit form ---
@app.route("/edit/<idno>")
def edit_student(idno):
    students = getall("students")
    student = getrecord("students", idno=idno)
    if student:
        return render_template("index.html", studentlist=students, student=student[0])
    return redirect(url_for("index"))


# --- Update student ---
@app.route("/update/<idno>", methods=["POST"])
def update_student(idno):
    lastname = request.form.get("lastname", "").strip()
    firstname = request.form.get("firstname", "").strip()
    course = request.form.get("course", "")
    level = request.form.get("level", "")

    if lastname and firstname:
        try:
            conn = connect('db/school.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students 
                SET lastname=?, firstname=?, course=?, level=? 
                WHERE idno=?
            """, [lastname, firstname, course, level, idno])
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Update error: {e}")
    
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)