from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = "../database/clinical_workflow.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return jsonify({"message": "Clinical Workflow Management System API"})


@app.route("/visits", methods=["GET"])
def get_visits():
    conn = get_connection()
    visits = conn.execute("""
        SELECT 
            visits.visit_id,
            patients.first_name,
            patients.last_name,
            visits.department,
            visits.provider,
            visits.status,
            visits.check_in_time,
            visits.discharge_time
        FROM visits
        JOIN patients ON visits.patient_id = patients.patient_id
        ORDER BY visits.check_in_time DESC
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in visits])


@app.route("/visits", methods=["POST"])
def create_visit():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients (first_name, last_name, date_of_birth, phone_number)
        VALUES (?, ?, ?, ?)
    """, (
        data["first_name"],
        data["last_name"],
        data["date_of_birth"],
        data["phone_number"]
    ))

    patient_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO visits (patient_id, department, provider, status, check_in_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        data["department"],
        data["provider"],
        "Checked In",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Visit created successfully"}), 201


@app.route("/visits/<int:visit_id>/status", methods=["PUT"])
def update_visit_status(visit_id):
    data = request.get_json()
    new_status = data["status"]

    discharge_time = None
    if new_status == "Discharged":
        discharge_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()

    if discharge_time:
        conn.execute("""
            UPDATE visits
            SET status = ?, discharge_time = ?
            WHERE visit_id = ?
        """, (new_status, discharge_time, visit_id))
    else:
        conn.execute("""
            UPDATE visits
            SET status = ?
            WHERE visit_id = ?
        """, (new_status, visit_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Visit status updated successfully"})


@app.route("/reports/visit-counts", methods=["GET"])
def visit_counts():
    conn = get_connection()
    results = conn.execute("""
        SELECT status, COUNT(*) AS total
        FROM visits
        GROUP BY status
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])


if __name__ == "__main__":
    app.run(debug=True)