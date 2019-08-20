from connection_manager import ConnectSQL
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello\n This is a students Api"

@app.route('/get_students')
def get_students():
    retJson = {"students": []}
    query = "select * from students"
    with ConnectSQL("Students") as manager:
        manager.exec(query)
        record = manager.fetchall()
        for row in record:
            retJson["students"].append({"name": row[1], "surname": row[2], "student_id": row[3]})
        return jsonify(retJson)

@app.route('/add_student', methods=["POST"])
def add_student():
    postedData = request.get_json()
    name = postedData["name"]
    surname = postedData["surname"]
    student_id = postedData["student_id"]
    id = postedData["id"]
    query = f"INSERT INTO students (id, name, surname, student_id) VALUES ('{id}', '{name}', '{surname}', '{student_id}')"
    with ConnectSQL("Students") as manager:
        manager.exec(query, commit=True)
        return jsonify({"Update": "success"}), 200
    return jsonify({"Update": "error"}), 400

@app.route('/update_student', methods=["PUT"])
def update_student():
    postedData = request.get_json()
    name = postedData["name"]
    surname = postedData["surname"]
    student_id = postedData["student_id"]
    is_present = f"SELECT student_id from students WHERE student_id = {student_id}"
    upd_record = f"UPDATE students SET name = '{name}', surname = '{surname}' WHERE student_id = {student_id}"
    with ConnectSQL("Students") as manager:
        manager.exec(is_present)
        if not manager.fetchall():
            return jsonify({"Update": "error", "Comments": "Student id is invalid"}), 400
        manager.exec(upd_record, commit=True)
    return jsonify({"Update": "success"}), 200

@app.route('/find_student', methods=["POST"])
def find_student():
    retJson = {"student": []}
    postedData = request.get_json()
    student_id = postedData["student_id"]
    is_present = f"SELECT name, surname, student_id from students WHERE student_id = {student_id}"
    with ConnectSQL("Students") as manager:
        manager.exec(is_present)
        record = manager.fetchall()
        for row in record:
            retJson["student"].append({"name": row[0], "surname": row[1], "student_id": row[2]})
        return jsonify(retJson), 200

@app.route('/all_info', methods=["POST"])
def all_info():
    retJson = {"student": [], "grades": []}
    postedData = request.get_json()
    student_id = postedData["student_id"]
    info = f"SELECT st.name, st.surname, st.student_id, f.faculty from students st " \
            f"JOIN faculty f on st.faculty_id = f.faculty_id " \
            f"WHERE st.student_id = {student_id}"

    grades = f"SELECT g.grade , s.subject from grades g " \
              f"JOIN subjects s on s.subject_id = g.subject_id "  \
              f"WHERE g.student_id = {student_id}"
    with ConnectSQL("Students") as manager:
        manager.exec(info)
        record = manager.fetchall()
        for row in record:
            retJson["student"].append({"name": row[0], "surname": row[1], "student_id": row[2],
                                        "faculty": row[3]})
        manager.exec(grades)
        record = manager.fetchall()
        for row in record:
            retJson["grades"].append({"subject": row[1], "grade": row[0]})
        return jsonify(retJson)

if __name__ == "__main__":
    app.run(debug=True)
