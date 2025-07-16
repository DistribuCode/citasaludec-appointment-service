# src/utils/availability_client.py

import httpx

async def is_doctor_available(user_id: str, jwt_token: str):
    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        url = f"http://availability-service:4010/availability/{user_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Puedes ajustar según lo que devuelva el controlador
            return len(data) > 0  # si hay disponibilidad
    except Exception as e:
        print("❌ Error consultando disponibilidad:", e)
        return False
