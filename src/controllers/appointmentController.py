from src.config.db import conn
from src.utils.rabbitmq import publish_appointment_created

async def get_appointments():
    cur = conn.cursor()
    cur.execute("SELECT id, patient, patient_name, disease, date FROM appointments")
    rows = cur.fetchall()
    cur.close()
    return [
        {
            "id": r[0],
            "patient": r[1],
            "patient_name": r[2],
            "disease": r[3],
            "date": r[4]
        }
        for r in rows
    ]

async def create_appointment(data):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO appointments (patient, patient_name, disease, date)
        VALUES (%s, %s, %s, %s) RETURNING id
        """,
        (data["patient"], data["patient_name"], data["disease"], data["date"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    # 👉 Aquí publicamos el evento en RabbitMQ
    event_payload = {
        "id": new_id,
        "patient": data["patient"],
        "patient_name": data["patient_name"],
        "disease": data["disease"],
        "date": str(data["date"])
    }
    publish_appointment_created(event_payload)

    return {"message": "Appointment created", "id": new_id}
