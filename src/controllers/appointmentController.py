from src.config.db import conn
from src.utils.rabbitmq import publish_appointment_created
from src.utils.availability_client import is_doctor_available

# ✅ FUNCIÓN PARA CREAR UNA CITA
async def create_appointment(data, token):  # Agregamos el token como parámetro
    doctor_id = data["patient"]  # o usa otra clave si no es el paciente

    # 🔍 1. Validar disponibilidad del doctor
    disponible = await is_doctor_available(doctor_id, token)
    if not disponible:
        return {"error": "Doctor no disponible"}, 400

    # ✅ 2. Guardar la cita si hay disponibilidad
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

    # 📣 3. Emitir evento a RabbitMQ
    event_payload = {
        "id": new_id,
        "patient": data["patient"],
        "patient_name": data["patient_name"],
        "disease": data["disease"],
        "date": str(data["date"])
    }
    publish_appointment_created(event_payload)

    return {"message": "Appointment created", "id": new_id}

# ✅ NUEVA FUNCIÓN PARA LISTAR CITAS
async def get_appointments():
    cur = conn.cursor()
    cur.execute("SELECT id, patient, patient_name, disease, date FROM appointments")
    rows = cur.fetchall()
    cur.close()

    citas = []
    for row in rows:
        citas.append({
            "id": row[0],
            "patient": row[1],
            "patient_name": row[2],
            "disease": row[3],
            "date": str(row[4])  
        })

    return citas
