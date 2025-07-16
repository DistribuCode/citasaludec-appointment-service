from src.config.db import conn
from src.utils.rabbitmq import publish_appointment_created
from src.utils.availability_client import is_doctor_available

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
