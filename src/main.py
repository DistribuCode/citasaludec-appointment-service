from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.routes import appointmentRoutes
from dotenv import load_dotenv
import os
print("🔐 JWT_SECRET cargado:", os.getenv("JWT_SECRET"))


load_dotenv()

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montamos las rutas bajo el prefijo
app.include_router(appointmentRoutes.router, prefix="/appointments")

# ==============================
# Configuración personalizada OpenAPI para añadir bearerAuth
# ==============================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Appointment Service API",
        version="1.0.0",
        description="API para agendar citas con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # para que todas las rutas requieran bearer por defecto en Swagger UI
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"bearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=4007, reload=True)
